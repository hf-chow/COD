from typing import Optional, Sequence
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

PROJECT_ID = "sia-gpt-405301"
LOCATION = "us"
OCR_PROCESSOR_DISPLAY_NAME = "test"
OCR_PROCESSOR_TYPE = "Document OCR"
OCR_PROCESSOR_ID = "3305d31f119e0903"
FORM_PARSER_PROCESSOR_DISPLAY_NAME = "tset_form_parser"
FORM_PARSER_PROCESSOR_TYPE = "Form Parser"
FORM_PARSER_PROCESSOR_ID = "9b9bf96b8e6ff3f9"
FORM_PARSER_PROCESSOR_VERSION = "pretrained-form-parser-v2.0-2022-11-10"

def process_document_form(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    # Read the table and form fields output from the processor
    # The form processor also contains OCR data. For more information
    # on how to parse OCR data please see the OCR sample.

    text = document.text
    print(f"Full document text: {repr(text)}\n")
    print(f"There are {len(document.pages)} page(s) in this document.")

    # Read the form fields and tables output from the processor
    for page in document.pages:
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"\nFound {len(page.tables)} table(s):")
        for table in page.tables:
            num_columns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_columns} columns and {num_rows} rows:")

            # Print header rows
            print("Columns:")
            print_table_rows(table.header_rows, text)
            # Print body rows
            print("Table body data:")
            print_table_rows(table.body_rows, text)

        print(f"\nFound {len(page.form_fields)} form field(s):")
        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            print(f"    * {repr(name.strip())}: {repr(value.strip())}")

    # Supported in version `pretrained-form-parser-v2.0-2022-11-10` and later.
    # For more information: https://cloud.google.com/document-ai/docs/form-parser
    if document.entities:
        print(f"Found {len(document.entities)} generic entities:")
        for entity in document.entities:
            print_entity(entity)
            # Print Nested Entities
            for prop in entity.properties:
                print_entity(prop)

    return document


def print_table_rows(
    table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        print(row_text)


def print_entity(entity: documentai.Document.Entity) -> None:
    # Fields detected. For a full list of fields for each processor see
    # the processor documentation:
    # https://cloud.google.com/document-ai/docs/processors-list
    key = entity.type_

    # Some other value formats in addition to text are availible
    # e.g. dates: `entity.normalized_value.date_value.year`
    text_value = entity.text_anchor.content
    confidence = entity.confidence
    normalized_value = entity.normalized_value.text
    print(f"    * {repr(key)}: {repr(text_value)}({confidence:.1%} confident)")

    if normalized_value:
        print(f"    * Normalized Value: {repr(normalized_value)}")


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )

pdf_path = "./samples/AXA SmartPlan Shop_Chi_SSQ-B-0123 (C-H265h) (002).pdf"
process_document_form(PROJECT_ID, LOCATION, FORM_PARSER_PROCESSOR_ID, FORM_PARSER_PROCESSOR_VERSION, pdf_path, mime_type="application/pdf")
