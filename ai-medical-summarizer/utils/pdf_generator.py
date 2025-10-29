from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class MedicalResearchPDFGenerator:
    def __init__(self, filename="medical_research_summary.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor='darkblue'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor='darkgreen'
        ))
        
        # Paper title style
        self.styles.add(ParagraphStyle(
            name='PaperTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=15,
            textColor='navy'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            firstLineIndent=20
        ))
        
        # Citation style
        self.styles.add(ParagraphStyle(
            name='Citation',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=10,
            leftIndent=20,
            textColor='gray'
        ))
    
    def add_title(self, title):
        """Add main title to the PDF"""
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        self.story.append(Spacer(1, 12))
    
    def add_header_info(self, query):
        """Add header information including query and date"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        self.story.append(Paragraph(f"<b>Research Query:</b> {query}", self.styles['CustomBody']))
        self.story.append(Paragraph(f"<b>Generated on:</b> {date_str}", self.styles['CustomBody']))
        self.story.append(Spacer(1, 20))
    
    def add_section_header(self, header):
        """Add a section header"""
        self.story.append(Paragraph(header, self.styles['SectionHeader']))
    
    def add_paper_content(self, paper):
        """Add content for a single research paper"""
        # Paper title and type
        title = paper.get('title', 'Unknown Title')
        paper_type = paper.get('type', 'Unknown Type').title()
        
        self.story.append(Paragraph(f"{title} ({paper_type})", self.styles['PaperTitle']))
        
        # Summary content
        summary = paper.get('summary', {})
        
        if 'causes' in summary and summary['causes']:
            self.story.append(Paragraph("<b>Causes:</b>", self.styles['CustomBody']))
            for cause in summary['causes']:
                self.story.append(Paragraph(f"• {cause}", self.styles['CustomBody']))
            self.story.append(Spacer(1, 6))
        
        if 'key_findings' in summary and summary['key_findings']:
            self.story.append(Paragraph("<b>Key Findings:</b>", self.styles['CustomBody']))
            for finding in summary['key_findings']:
                self.story.append(Paragraph(f"• {finding}", self.styles['CustomBody']))
            self.story.append(Spacer(1, 6))
        
        if 'common treatment methods' in summary and summary['common treatment methods']:
            self.story.append(Paragraph("<b>Common Treatment Methods:</b>", self.styles['CustomBody']))
            for treatment in summary['common treatment methods']:
                self.story.append(Paragraph(f"• {treatment}", self.styles['CustomBody']))
            self.story.append(Spacer(1, 6))
        
        if 'limitations of certain treatments' in summary and summary['limitations of certain treatments']:
            self.story.append(Paragraph("<b>Treatment Limitations:</b>", self.styles['CustomBody']))
            for limitation in summary['limitations of certain treatments']:
                self.story.append(Paragraph(f"• {limitation}", self.styles['CustomBody']))
            self.story.append(Spacer(1, 6))
        
        if 'latest treatments' in summary and summary['latest treatments']:
            self.story.append(Paragraph("<b>Latest Treatments:</b>", self.styles['CustomBody']))
            for treatment in summary['latest treatments']:
                self.story.append(Paragraph(f"• {treatment}", self.styles['CustomBody']))
            self.story.append(Spacer(1, 6))
        
        # Citation
        if 'citation' in paper:
            self.story.append(Paragraph(f"<b>Citation:</b> {paper['citation']}", self.styles['Citation']))
        
        self.story.append(Spacer(1, 15))
    
    def generate_pdf(self, data):
        """Generate the complete PDF from data"""
        try:
            # Add title
            self.add_title("Medical Research Summary Report")
            
            # Add header info
            query = data.get('query', 'Unknown Query')
            self.add_header_info(query)
            
            # Add papers section
            papers = data.get('papers', [])
            if papers:
                self.add_section_header(f"Research Papers ({len(papers)} found)")
                
                for i, paper in enumerate(papers, 1):
                    self.story.append(Paragraph(f"Paper {i}:", self.styles['SectionHeader']))
                    self.add_paper_content(paper)
                    
                    # Add page break between papers (except for the last one)
                    if i < len(papers):
                        self.story.append(PageBreak())
            else:
                self.story.append(Paragraph("No research papers found for this query.", self.styles['CustomBody']))
            
            # Build the PDF
            self.doc.build(self.story)
            logger.info(f"PDF generated successfully: {self.filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            return False

def generate_medical_research_pdf(data, filename=None):
    """
    Main function to generate PDF from medical research data
    
    Args:
        data: Dictionary containing the research data (same format as JSON output)
        filename: Optional custom filename for the PDF
    
    Returns:
        bool: True if successful, False otherwise
    """
    if filename is None:
        # Generate filename based on query and timestamp
        query = data.get('query', 'medical_research')
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_query = safe_query.replace(' ', '_')[:50]  # Limit length
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"medical_research_{safe_query}_{timestamp}.pdf"
    
    generator = MedicalResearchPDFGenerator(filename)
    return generator.generate_pdf(data)

# Example usage
if __name__ == "__main__":
    # Test data
    test_data = {
        "query": "teach me about brain cancer",
        "papers": [
            {
                "title": "Recent Advances in Brain Cancer Treatment",
                "type": "review",
                "summary": {
                    "causes": ["Genetic mutations", "Environmental factors"],
                    "key_findings": ["New immunotherapy approaches show promise"],
                    "common treatment methods": ["Surgery", "Chemotherapy", "Radiation therapy"],
                    "limitations of certain treatments": ["Side effects", "Limited effectiveness"],
                    "latest treatments": ["CAR-T cell therapy", "Targeted molecular therapy"]
                },
                "citation": "[Recent Advances in Brain Cancer Treatment](http://example.com)"
            }
        ]
    }
    
    success = generate_medical_research_pdf(test_data, "test_medical_research.pdf")
    print(f"PDF generation {'successful' if success else 'failed'}")
