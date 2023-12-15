from google.cloud import documentai_v1beta3 as documentai

PROJECT_ID = "sia-gpt-405301"
LOCATION = "us"
OCR_PROCESSOR_DISPLAY_NAME = "test"
OCR_PROCESSOR_TYPE = "Document OCR"
OCR_PROCESSOR_ID = "3305d31f119e0903"
FORM_PARSER_PROCESSOR_DISPLAY_NAME = "tset_form_parser"
FORM_PARSER_PROCESSOR_TYPE = "Form Parser"
FORM_PARSER_PROCESSOR_ID = "9b9bf96b8e6ff3f9"

def form_parser_pdf(pdf_path, project_id, location, processor_id):
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
    extraction_params = documentai.TableExtractionParams()
    form_parser_params = documentai.FormExtractionParams(
            table_extraction_params = extraction_params
            )

    # Process the document
    request = documentai.ProcessDocumentRequest(
            parent="projects/project_id/locations/location-id",
            document = document,
            form_extraction_params=form_parser_params)
    response = client.process_document(request=request)

    content = response.document
    for page in response.pages:
        for form_field in page.form_fields:
            print("BBox ", form_field.field_name.bounding_poly)
        for table in page.tables:
            print("Table")
            for row in table.header_rows:
                for cell in row.cells:
                    print("Header ", cell.text)
            for row in table.body_rows:
                for cell in row.cells:
                    print("Body ", cell.text)
    
    return content.text

pdf_path = "./samples/AXA SmartPlan Shop_Chi_SSQ-B-0123 (C-H265h) (002).pdf"

form_parser_output = form_parser_pdf(pdf_path, PROJECT_ID, LOCATION, FORM_PARSER_PROCESSOR_ID)

