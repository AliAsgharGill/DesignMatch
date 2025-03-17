import os
from pathlib import Path

import weasyprint
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

# Create APIRouter instance
router = APIRouter()


# Define a Pydantic model for validation results
class ValidationResult(BaseModel):
    similarity_score: float
    color_correlation: float
    layout_mismatches: list
    font_size_mismatches: list
    button_size_mismatches: list


# Initialize Jinja2 environment
template_env = Environment(
    loader=FileSystemLoader("templates"),  # Folder containing Jinja2 templates
)


# Use router instead of app for the endpoint
@router.post("/generate-report")
async def generate_report(validation_results: ValidationResult):
    try:
        # Create a report directory if it doesn't exist
        report_dir = Path("reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        # Render the HTML template with validation results
        template = template_env.get_template("report_template.html")

        # Create a dictionary of validation data to pass to the template
        report_data = {
            "similarity_score": validation_results.similarity_score,
            "color_correlation": validation_results.color_correlation,
            "layout_mismatches": validation_results.layout_mismatches,
            "font_size_mismatches": validation_results.font_size_mismatches,
            "button_size_mismatches": validation_results.button_size_mismatches,
        }

        # Generate HTML report
        html_content = template.render(report_data)

        # Save HTML report to a file
        report_path_html = report_dir / "report.html"
        with open(report_path_html, "w") as f:
            f.write(html_content)

        # Optionally, convert the HTML to PDF
        pdf_path = report_dir / "report.pdf"
        weasyprint.HTML(report_path_html).write_pdf(pdf_path)

        # Return a downloadable link to the generated report (PDF in this case)
        return {"download_link": str(pdf_path)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example HTML template (report_template.html) in the 'templates' folder
