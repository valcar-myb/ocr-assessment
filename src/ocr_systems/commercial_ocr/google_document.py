"""
Google Cloud Document AI OCR implementation
"""

from typing import Dict, Any
from ..models import OCRSystem


class GoogleDocumentOCR(OCRSystem):
    """Google Cloud Document AI OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model = None
        self._init_predictor()
    
    def _init_predictor(self):
        """Initialize Google Document AI client"""
        try:
            from google.cloud import documentai
            from google.api_core.client_options import ClientOptions
            from google.oauth2 import service_account
            
            location = self.config.get('location', 'us')
            
            # Check if service account credentials are provided
            if 'type' in self.config and 'project_id' in self.config:
                # Use service account credentials from config
                credentials = service_account.Credentials.from_service_account_info({
                    'type': self.config.get('type'),
                    'project_id': self.config.get('project_id'),
                    'private_key_id': self.config.get('private_key_id'),
                    'private_key': self.config.get('private_key', '').replace('\\n', '\n'),
                    'client_email': self.config.get('client_email'),
                    'client_id': str(self.config.get('client_id')),
                    'auth_uri': self.config.get('auth_uri'),
                    'token_uri': self.config.get('token_uri'),
                    'auth_provider_x509_cert_url': self.config.get('auth_provider_x509_cert_url'),
                    'client_x509_cert_url': self.config.get('client_x509_cert_url')
                })
                self.model = documentai.DocumentProcessorServiceClient(
                    client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com"),
                    credentials=credentials
                )
            else:
                # Use default credentials
                self.model = documentai.DocumentProcessorServiceClient(
                    client_options=ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
                )
        except ImportError:
            print("Google Cloud Document AI not installed. Please install with: pip install google-cloud-documentai")
            raise
        except Exception as e:
            print(f"Error initializing Google Document AI client: {e}")
            raise
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from Google Document AI"""
        try:
            from google.cloud import documentai
            from google.protobuf.json_format import MessageToJson
            import json
            
            # Build processor name
            processor_version_id = self.config.get('processor_version_id')
            if processor_version_id:
                name = self.model.processor_version_path(
                    project=self.config.get('project_id'),
                    location=self.config.get('location', 'us'),
                    processor=self.config.get('processor_id'),
                    processor_version=processor_version_id
                )
            else:
                name = self.model.processor_path(
                    project=self.config.get('project_id'),
                    location=self.config.get('location', 'us'),
                    processor=self.config.get('processor_id')
                )
            
            # Read image file
            with open(image_path, 'rb') as image:
                image_content = image.read()
            
            # Determine MIME type from file extension
            img_type = image_path.split('.')[-1].lower()
            mime_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            mime_type = mime_type_map.get(img_type, 'image/jpeg')
            
            # Create raw document
            raw_document = documentai.RawDocument(
                content=image_content,
                mime_type=mime_type
            )
            
            # Create process options
            process_options = documentai.ProcessOptions(
                individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
                    pages=[1]
                )
            )
            
            # Call Google Document AI API
            result = self.model.process_document(
                request=documentai.ProcessRequest(
                    name=name,
                    raw_document=raw_document,
                    field_mask=self.config.get('field_mask'),
                    process_options=process_options
                )
            )
            
            # Convert protobuf response to dict
            json_result = json.loads(MessageToJson(result._pb))
            
            # Remove image data to save space
            if 'document' in json_result and 'pages' in json_result['document']:
                for page in json_result['document']['pages']:
                    if 'image' in page:
                        del page['image']
            
            return json_result
        except Exception as e:
            print(f"Error extracting raw output with Google Document AI: {e}")
            return {}
