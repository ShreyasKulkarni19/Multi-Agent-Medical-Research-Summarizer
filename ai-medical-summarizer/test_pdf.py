#!/usr/bin/env python3
"""
Test script to verify PDF generation functionality
"""

from utils.pdf_generator import generate_medical_research_pdf
import json

# Sample test data
test_data = {
    "query": "What are the latest treatments for diabetes?",
    "papers": [
        {
            "title": "Innovative Diabetes Management Approaches",
            "link": "https://example.com/diabetes-study",
            "type": "clinical trial",
            "summary": {
                "causes": [
                    "Genetic predisposition",
                    "Insulin resistance",
                    "Environmental factors"
                ],
                "key_findings": [
                    "New insulin formulations show improved glycemic control",
                    "Continuous glucose monitoring reduces complications",
                    "Personalized treatment plans increase adherence"
                ],
                "common treatment methods": [
                    "Insulin therapy",
                    "Metformin treatment",
                    "Lifestyle modifications",
                    "Regular blood glucose monitoring"
                ],
                "limitations of certain treatments": [
                    "Insulin injections can be inconvenient",
                    "Side effects include weight gain",
                    "Cost barriers for continuous monitoring"
                ],
                "latest treatments": [
                    "Smart insulin patches",
                    "Artificial pancreas systems",
                    "GLP-1 receptor agonists",
                    "SGLT-2 inhibitors"
                ]
            },
            "citation": "[Innovative Diabetes Management Approaches](https://example.com/diabetes-study)"
        },
        {
            "title": "Breakthrough Gene Therapy for Type 1 Diabetes",
            "link": "https://example.com/gene-therapy",
            "type": "review",
            "summary": {
                "causes": [
                    "Autoimmune destruction of beta cells"
                ],
                "key_findings": [
                    "Gene therapy shows promise in beta cell regeneration",
                    "Immunomodulation can prevent further autoimmune damage"
                ],
                "common treatment methods": [
                    "Intensive insulin therapy",
                    "Islet cell transplantation"
                ],
                "limitations of certain treatments": [
                    "Limited donor islets available",
                    "Immunosuppression side effects"
                ],
                "latest treatments": [
                    "CRISPR-edited beta cells",
                    "Stem cell-derived islets",
                    "Immunoprotective encapsulation"
                ]
            },
            "citation": "[Breakthrough Gene Therapy for Type 1 Diabetes](https://example.com/gene-therapy)"
        }
    ]
}

def test_pdf_generation():
    """Test the PDF generation with sample data"""
    print("Testing PDF generation...")
    
    # Generate PDF with custom filename
    filename = "test_diabetes_research_report.pdf"
    success = generate_medical_research_pdf(test_data, filename)
    
    if success:
        print(f"✅ PDF generated successfully: {filename}")
        print("You can check the generated PDF file.")
    else:
        print("❌ PDF generation failed")
        return False
    
    return True

if __name__ == "__main__":
    test_pdf_generation()
