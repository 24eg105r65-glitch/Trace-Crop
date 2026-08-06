import os
import glob
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_page_number(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def set_font(run, size=12, bold=False):
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    run.font.size = Pt(size)
    run.bold = bold

def add_heading(doc, text, level=1):
    if level == 1:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        set_font(run, 16, bold=True)
    elif level == 2:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(10)
        run = p.add_run(text)
        set_font(run, 14, bold=True)
    return p

def add_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    set_font(run, 12, bold=bold)
    return p

def add_image_with_caption(doc, image_path, caption):
    if os.path.exists(image_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(image_path, width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.line_spacing = 1.5
        run_cap = p_cap.add_run(caption)
        set_font(run_cap, 12, bold=False)
    else:
        add_paragraph(doc, f"[Image Placehoder: {image_path}]\n{caption}")

def add_code_snippet(doc, title, filepath):
    add_heading(doc, title, level=2)
    if not os.path.exists(filepath):
        add_paragraph(doc, f"File {filepath} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    
    # Set column widths
    table.columns[0].width = Inches(0.5)
    table.columns[1].width = Inches(5.5)
    
    row = table.rows[0]
    line_nums = "\n".join(str(i+1) for i in range(len(lines)))
    code_text = "".join(lines)
    
    row.cells[0].text = line_nums
    row.cells[1].text = code_text
    
    for idx, cell in enumerate(row.cells):
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.name = 'Courier New'
                run.font.size = Pt(9)
            paragraph.paragraph_format.line_spacing = 1.0

def generate_report():
    doc = Document()

    # Apply global styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # -----------------------------
    # Title Page
    # -----------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("A Summer Internship Project\nReport on\n")
    set_font(run, 12)
    run = p.add_run("“TraceCrop: Supply Chain Intelligence Platform”\n\n")
    set_font(run, 16, bold=True)
    
    run = p.add_run("Submitted in partial fulfilment of the Requirements for the\naward of the Degree of\nBACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE & ENGINEERING\n\nBy\n")
    set_font(run, 12, bold=True)
    
    run = p.add_run("ADABALA PUSHKARAN\n24EG105R65\n\n")
    set_font(run, 12, bold=True)
    
    run = p.add_run("Under the Guidance of\nMrs. Y. Ashwini Sharma\n\n")
    set_font(run, 12, bold=True)
    
    if os.path.exists("anurag_logo.png"):
        run_logo = p.add_run()
        run_logo.add_picture("anurag_logo.png", width=Inches(1.5))
        p.add_run("\n\n")
        
    run = p.add_run("Department of Computer Science & Engineering\nANURAG UNIVERSITY\nGHATKESAR (M), MEDCHAL DISTRICT,\nHyderabad-88\nAcademic Year: 2025-2026\n")
    set_font(run, 12, bold=True)
    
    doc.add_page_break()
    
    # -----------------------------
    # Certificate
    # -----------------------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ANURAG UNIVERSITY\nHyderabad-500 088\nDepartment of Computer Science & Engineering\n\n")
    set_font(run, 14, bold=True)
    
    if os.path.exists("anurag_logo.png"):
        run_logo = p.add_run()
        run_logo.add_picture("anurag_logo.png", width=Inches(1.5))
        p.add_run("\n\n")
        
    run = p.add_run("CERTIFICATE\n\n")
    set_font(run, 16, bold=True)
    
    cert_text = (
        "I, ADABALA PUSHKARAN, bearing hall ticket number, 24EG105R65, hereby declare that the "
        "project report entitled “TraceCrop: Supply Chain Intelligence Platform” Department of "
        "Computer Science & Engineering, Anurag University, Hyderabad, is submitted in partial fulfilment "
        "of the requirement for the award of the degree of Bachelor of Technology in Computer Science & "
        "Engineering.\n\n"
        "This is a record of bonafide work carried out by me and the results embodied in this project "
        "report have not been submitted to any other university or institute for the award of any other "
        "degree or diploma.\n\n\n\n"
    )
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p2.paragraph_format.line_spacing = 1.5
    run = p2.add_run(cert_text)
    set_font(run, 12)
    
    # Signatures
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Signature of The Guide"
    table.cell(0, 1).text = "ADABALA PUSHKARAN"
    table.cell(1, 0).text = "Mrs. Y. Ashwini Sharma"
    table.cell(1, 1).text = "24EG105R65"
    
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    set_font(run, 12, bold=True)
                    
    doc.add_page_break()

    # Enable Page Numbers after Index
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(footer_para.add_run())

    # -----------------------------
    # Table of Contents
    # -----------------------------
    add_heading(doc, "TABLE OF CONTENTS")
    toc_data = [
        ("1", "Acknowledgement", "1"),
        ("2", "Declaration", "2"),
        ("3", "Abstract", "3"),
        ("4", "Introduction", "4"),
        ("5", "Problem Statement", "5"),
        ("6", "Objectives", "6"),
        ("7", "Scope of the Project", "7"),
        ("8", "Existing System", "8"),
        ("9", "Proposed System", "10"),
        ("10", "Software & Hardware Requirements", "12"),
        ("11", "System Design", "13"),
        ("12", "Flowchart & Algorithm", "15"),
        ("13", "Modules Description", "17"),
        ("14", "Implementation", "20"),
        ("15", "Results / Output Screens", "22"),
        ("16", "Advantages & Limitations", "26"),
        ("17", "Future Enhancements", "27"),
        ("18", "Conclusion", "28"),
        ("19", "References", "29"),
        ("20", "Source Code", "30")
    ]
    
    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.style = 'Table Grid'
    hdr_cells = toc_table.rows[0].cells
    hdr_cells[0].text = 'S.No.'
    hdr_cells[1].text = 'Topic / Chapter'
    hdr_cells[2].text = 'Page No.'
    
    for item in toc_data:
        row_cells = toc_table.add_row().cells
        row_cells[0].text = item[0]
        row_cells[1].text = item[1]
        row_cells[2].text = item[2]
        
    for row in toc_table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    set_font(run, 12)
    
    doc.add_page_break()

    # -----------------------------
    # Acknowledgement
    # -----------------------------
    add_heading(doc, "ACKNOWLEDGEMENT")
    ack_text = (
        "I would like to express my sincere thanks and deep sense of gratitude to project "
        "supervisor Mrs. Y. Ashwini Sharma, for her constant encouragement and inspiring guidance "
        "without which this project could not have been completed. Her critical reviews and "
        "constructive comments improved our grasp of the subject and steered to the fruitful "
        "completion of the work. Her patience, guidance and encouragement made this project "
        "possible.\n\n"
        "I would like to express my sincere gratitude to Dr. Archana Mantri, Vice Chancellor, "
        "Anurag University and Dr. P. Bhaskara Reddy, Registrar, Anurag University for their "
        "encouragement and support.\n\n"
        "I would like to express my special thanks to Dr. V. Vijaya Kumar, Dean School of "
        "Engineering, Anurag University, for his encouragement and timely support in our B.Tech "
        "program.\n\n"
        "I would like to acknowledge my sincere gratitude for the support extended by Dr. G. "
        "Vishnu Murthy, Dean, Department of Computer Science Engineering, Anurag University. We "
        "also express my deep sense of gratitude to Dr. P. Ravinder Rao, academic coordinator, "
        "whose research expertise and commitment to the highest standards continuously "
        "motivated us during the crucial stage of our project work.\n\n\n"
        "ADABALA PUSHKARAN\n24EG105R65\n"
    )
    add_paragraph(doc, ack_text)
    doc.add_page_break()
    
    # -----------------------------
    # Declaration
    # -----------------------------
    add_heading(doc, "DECLARATION")
    dec_text = (
        "I hereby declare that the project entitled “TraceCrop: Supply Chain Intelligence Platform” "
        "submitted to the Department of Computer Science and Engineering is an original "
        "work carried out by me under the guidance Mrs. Y. Ashwini Sharma. The work presented in "
        "this report has not been submitted elsewhere for the award of any degree.\n\n\n"
        "ADABALA PUSHKARAN\n24EG105R65\n"
    )
    add_paragraph(doc, dec_text)
    doc.add_page_break()

    # -----------------------------
    # Content Generation - Padding out to 50 pages
    # -----------------------------
    
    chapters = [
        ("Chapter 1: Abstract", 
         "TraceCrop is a state-of-the-art supply chain intelligence platform designed to provide granular tracking, real-time data fusion, and absolute transparency across complex agricultural and enterprise logistics networks.\n\n"
         "The platform bridges the gap between fragmented agricultural supply networks and digital tracking, utilizing Firebase real-time infrastructure to ensure instant synchronization of logistical data. "
         "By implementing a robust role-based dashboard system, the platform provides tailored interfaces for farmers, distributors, retailers, and end consumers.\n\n"
         "Through these customized interfaces, TraceCrop effectively tackles the limitations of static supply chain registries, translating real-world supply movements into digital footprints that can be verified and audited continuously. "
         "This comprehensive approach ensures that every participant in the supply chain maintains a unified, immutable source of truth for all transactions and quality checks."),
         
        ("Chapter 2: Introduction", 
         "The digital transformation of supply chain networks has necessitated the creation of modern tracking platforms. TraceCrop acts as a neural-driven logistics engine that eliminates blind spots.\n\n"
         "Historically, agricultural and enterprise supply chains operated on disparate systems, introducing significant latencies and opportunities for fraud or data loss. "
         "TraceCrop resolves these operational bottlenecks by integrating real-time telemetry and a unified cloud-based tracking console. "
         "The platform employs an intuitive frontend architecture built on Tailwind CSS, which ensures high usability and minimal learning curves for all stakeholders.\n\n"
         "At the application layer, TraceCrop leverages Firebase Firestore, ensuring strict data validation and rapid query response times. "
         "This decoupled architecture maximizes scalability while minimizing latency across the entire platform. "
         "Ultimately, TraceCrop represents a significant leap forward in supply chain intelligence, providing secure, cross-platform compatibility and real-time oversight."),
         
        ("Chapter 3: Problem Statement", 
         "Traditional supply chains operate in silos, leading to significant visibility gaps. Without a unified ledger of truth, stakeholders struggle to verify authenticity and track items in real time.\n\n"
         "Because participants often rely on paper-based records or disconnected digital databases, tracking the origin, transit, and quality of goods becomes a fragmented and error-prone process. "
         "This lack of automation forces administrative teams to manually reconcile transaction histories, compounding inefficiencies and introducing significant data latency.\n\n"
         "To eliminate these inefficiencies, a modern tracking framework must integrate real-time logging, strict access controls, and automated compliance tracking. "
         "TraceCrop is engineered to directly address these systemic vulnerabilities by providing an immutable, real-time digital tracking infrastructure."),
         
        ("Chapter 4: Objectives", 
         "The overarching objective of the TraceCrop project is to engineer, deploy, and evaluate a highly secure, low-latency supply chain intelligence platform.\n\n"
         "Specific goals include:\n"
         "(1) Developing an intelligent, real-time tracking portal to capture logistical movements and quality checks.\n"
         "(2) Implementing role-based dashboards tailored for farmers, distributors, retailers, and quality inspectors.\n"
         "(3) Designing a scalable, cloud-based data architecture using Firebase Firestore for persistent, immutable logging.\n"
         "(4) Integrating visual analytics and tracking history to give stakeholders end-to-end visibility.\n"
         "(5) Ensuring cross-platform accessibility through a responsive, mobile-first frontend design."),
         
        ("Chapter 5: Scope of the Project", 
         "The operational scope of TraceCrop is organized into a decentralized, multi-tiered architecture tailored for various supply chain participants.\n\n"
         "The system begins with a secure authentication sequence, unlocking access to specialized frontend layouts. Farmers can log harvest data, distributors can update transit statuses, and quality inspectors can record compliance metrics. "
         "Behind the scenes, the platform administrators maintain operational visibility through centralized tracking logs and user management workflows.\n\n"
         "To ensure data integrity, the application enforces strict read/write security rules at the database level. "
         "The infrastructure is purposely optimized for rapid execution and seamless cross-platform compatibility, achieving maximum operational efficiency without relying on complex, monolithic legacy systems."),
         
        ("Chapter 6: Existing System", 
         "Conventional supply chain tracking systems operate largely as fragmented registries that place a heavy burden of manual data entry on untrained users.\n\n"
         "This disconnect is closely mirrored by a complete lack of technical integration in back-office administration, where different stakeholders maintain entirely independent records. "
         "The absence of a centralized, real-time synchronization protocol means that data is often out-of-date or contradictory by the time it reaches the end consumer.\n\n"
         "To overcome these compounding infrastructure failures, modern systems must shift away from localized databases toward a highly visual, deterministic cloud model, which TraceCrop actively implements."),
         
        ("Chapter 7: Proposed System", 
         "The proposed TraceCrop system introduces an advanced, interactive tracking pipeline engineered specifically to resolve the communication bottlenecks of conventional supply chains.\n\n"
         "By rendering detailed, responsive web interfaces and utilizing Firebase's real-time capabilities, the frontend empowers users to seamlessly log and retrieve data points instantly. "
         "These data points are processed by a centralized cloud infrastructure that enforces strict validation rules and security protocols.\n\n"
         "Concurrently, the integrated dashboards automate the visualization of this data, transparently breaking down logistical journeys and quality metrics. "
         "These clean transaction histories provide an accurate, real-time reflection of the supply chain's status to all authorized parties."),
         
        ("Chapter 8: Software & Hardware Requirements", 
         "The developer and client environment specifications are structured to support rapid execution, responsive layouts, and cross-platform compatibility.\n\n"
         "1. Software Core Stack: The application is built entirely around modern web technologies, comprising HTML5, CSS3, JavaScript, and Tailwind CSS for the frontend, with Firebase handling backend services.\n"
         "2. Backend Server Environment: Firebase Firestore for NoSQL data persistence and Firebase Hosting for application delivery.\n"
         "3. Frontend Client Environment: A responsive, mobile-first design leveraging Tailwind CSS for rapid styling and layout configuration.\n"
         "4. Client Device Requirements: End-users can access the portal using any modern web browser (such as Chrome, Firefox, or Safari) that fully supports modern JavaScript and CSS grid/flexbox layouts."),
         
        ("Chapter 9: System Design", 
         "The database design is implemented using Firebase Firestore, enforcing strict validation through comprehensive security rules for primary data collections.\n\n"
         "The tracking schema is designed to capture essential logistical milestones, securely storing unique shipment identifiers, timestamps, and quality metrics. "
         "Additionally, role-based schemas govern user profiles, ensuring that distributors cannot overwrite farmer data, and consumers are restricted to read-only views.\n\n"
         "The system's routing logic mirrors this organized database structure by dynamically updating frontend components based on real-time snapshot listeners. "
         "This ensures that all connected clients receive updates instantaneously, maintaining synchronization across the entire network."),
         
        ("Chapter 10: Flowchart & Algorithm", 
         "The core tracking algorithm executes a secure data propagation routine whenever a new shipment is initialized or its status is updated.\n\n"
         "Before any logistical data is persisted to Firestore, the client-side logic processes the input, validates the data format, and attaches cryptographic authentication tokens. "
         "This multi-pass validation ensures that only authorized entities can mutate the supply chain ledger.\n\n"
         "Upon receiving a write request, the Firebase security rules evaluate the user's role and the document's current state. "
         "If the conditions are met, the database state is mutated, and the new data is automatically broadcasted to all active listeners on the network."),
         
        ("Chapter 11: Modules Description", 
         "The single-page application is structured into several core operational modules. "
         "The Authentication module manages the validation of user credentials to secure initial platform entry.\n\n"
         "The Role-Based Dashboards serve as the primary operational hubs, consolidating vital tracking data, quality metrics, and historical logs into unified views tailored for Farmers, Distributors, and Retailers. "
         "The Consumer Viewer module acts as the public-facing transparency layer, allowing end-users to scan or search for product origins and view the complete, immutable journey of their goods.\n\n"
         "Administrative workflows are handled by the Admin configuration, providing platform orchestrators with comprehensive operational analytics and system audit tracking."),
         
        ("Chapter 12: Implementation", 
         "Implementation began by establishing a unified project directory and configuring the Firebase environment. "
         "The frontend setup utilized robust HTML structures and Tailwind CSS to ensure a consistent, premium visual design across all modules.\n\n"
         "Application logic was dynamically managed using vanilla JavaScript to map core data structures to specific UI components for seamless transitions. "
         "Data fetching and mutation were directed to the Firebase backend through authenticated SDK calls, securing the communication between the client and the cloud database.\n\n"
         "Finally, the development workflow was streamlined through iterative testing of the Firestore security rules, ensuring that the application logic properly restricted access based on user roles and data states.")
    ]

    for title, text in chapters:
        add_heading(doc, title)
        add_paragraph(doc, text)
        doc.add_page_break()

    # -----------------------------
    # Results / Output Screens
    # -----------------------------
    add_heading(doc, "Chapter 13: Results / Output Screens")
    for i in range(1, 10):
        add_heading(doc, f"Result 13.{i}: Module Interface View", level=2)
        desc = (
            f"This screenshot illustrates the functional user interface of the TraceCrop platform. "
            f"The layout is optimized for rapid data ingestion and visual clarity. "
            f"It displays real-time tracking metrics and interactive components for the users. "
            f"This addresses the core requirements specified in the project scope by delivering an intuitive experience."
        )
        add_image_with_caption(doc, f"placeholder_image_{i}.png", desc)
        doc.add_page_break()

    # -----------------------------
    # Final Chapters
    # -----------------------------
    add_heading(doc, "Chapter 14: Advantages & Limitations")
    add_paragraph(doc, "The proposed TraceCrop platform offers several key advantages over traditional systems:\n"
                       "(1) Real-time logistical tracking that connects origin points to final consumer destinations.\n"
                       "(2) Highly secure and automated data validation workflows.\n"
                       "(3) Role-based access controls that ensure data integrity and prevent unauthorized mutations.\n\n"
                       "The limitations of the current implementation include:\n"
                       "(1) The application requires a stable network connection for real-time Firebase syncing.\n"
                       "(2) Hardware dependencies for advanced tracking (e.g., IoT sensors) are not fully integrated in the baseline software model.")
    doc.add_page_break()

    add_heading(doc, "Chapter 15: Future Enhancements")
    add_paragraph(doc, "Future development cycles will focus on integrating full-scale IoT sensor pipelines for automated temperature and humidity tracking during transit.\n\n"
                       "Additionally, the platform plans to incorporate AI-driven predictive analytics to forecast supply chain delays and suggest optimal routing adjustments. "
                       "Cloud storage integration will be expanded to support the attachment of high-resolution quality inspection reports and legal documentation directly to shipment records.")
    doc.add_page_break()

    add_heading(doc, "Chapter 16: Conclusion")
    add_paragraph(doc, "The TraceCrop portal successfully demonstrates the integration of modern cloud database telemetry, real-time data visualization, and secure access controls. "
                       "By replacing static, siloed registries with an interactive, role-based tracking engine, the platform significantly increases operational transparency and stakeholder engagement.\n\n"
                       "The automated data syncing and robust security rules protect logistical resources, presenting a viable and secure design for modern supply chain management. "
                       "In conclusion, the project validates that the proposed portal provides a low-latency, highly secure, and intuitive intelligence service that is fully compliant with modern data architecture standards.")
    doc.add_page_break()

    add_heading(doc, "Chapter 17: References")
    add_paragraph(doc, "1. Firebase Manual and Cloud Firestore Documentation. Official Database Schema Guidelines, 2025.\n"
                       "2. Tailwind CSS Documentation. Modern Utility-First CSS Framework Architecture, 2025.\n"
                       "3. JavaScript and Web API Design Standards. Client-Side Application Integration, 2025.\n"
                       "4. Supply Chain Intelligence and Tracking Protocols. Industry Standards, 2025.")
    doc.add_page_break()

    # -----------------------------
    # Source Code (50 pages total goal)
    # -----------------------------
    add_heading(doc, "Chapter 18: Source Code")
    
    files = glob.glob("**/*.html", recursive=True) + glob.glob("**/*.js", recursive=True) + glob.glob("**/*.css", recursive=True) + glob.glob("**/*.json", recursive=True) + glob.glob("**/*.rules", recursive=True)
    
    for filepath in files[:40]: # increased limit to ensure adequate page count without repetitions
        if "node_modules" not in filepath and ".git" not in filepath:
            add_code_snippet(doc, f"Source Code: {filepath}", filepath)
            doc.add_page_break()

    # Save the document
    doc.save("TraceCrop_Project_Report.docx")
    print("Report generated successfully as TraceCrop_Project_Report.docx")

if __name__ == "__main__":
    generate_report()
