from google.cloud import documentai_v1beta3 as documentai

PROJECT_ID = "sia-gpt-405301"
LOCATION = "us"
PROCESSOR_DISPLAY_NAME = "test"
PROCESSOR_TYPE = "Document OCR"
PROCESSOR_ID = "3305d31f119e0903"

def parse_pdf(pdf_path, project_id=PROJECT_ID, location=LOCATION, processor_id=PROCESSOR_ID):
    project_id = project_id
    location = location

    client = documentai.DocumentProcessorServiceClient()

    # Configure the processor
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the PDF file
    with open(pdf_path, "rb") as pdf_file:
        input_content = pdf_file.read()

    # Enable tokenization
    document = documentai.Document(content=input_content,
                                   mime_type="application/pdf")

    # Process the document
    request = documentai.ProcessRequest(name=processor_name, document=document)
    response = client.process_document(request=request)

    content = response.document
    
    print("Parsing successful!")
    print("The document content the following text")
    print(content.text)

    return content.text

pdf_path = "./samples/AXA SmartPlan Shop_Chi_SSQ-B-0123 (C-H265h) (002).pdf"
results = parse_pdf(pdf_path)
