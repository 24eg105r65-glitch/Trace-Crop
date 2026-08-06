import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fpdf import FPDF
import os

# 1. Create Block Diagram using matplotlib
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('off')

# draw boxes and arrows
blocks = ["Farmer\n(Data Origin)", "Distributor\n(Transit)", "Quality Control\n(Verification)", "Retailer\n(Stock)", "Consumer\n(Transparency)"]
x_centers = [1, 3.5, 6, 8.5, 11]
y_center = 2
box_width = 1.8
box_height = 1.0

for i, (text, x) in enumerate(zip(blocks, x_centers)):
    # Create fancy bounding box
    rect = patches.FancyBboxPatch((x - box_width/2, y_center - box_height/2), box_width, box_height, 
                                  boxstyle="round,pad=0.1,rounding_size=0.1", 
                                  linewidth=2, edgecolor='#10b981', facecolor='#e6fcf5')
    ax.add_patch(rect)
    ax.text(x, y_center, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#00422b')
    
    if i < len(blocks) - 1:
        # Draw arrow
        ax.annotate('', xy=(x_centers[i+1] - box_width/2 - 0.1, y_center), 
                    xytext=(x + box_width/2 + 0.1, y_center),
                    arrowprops=dict(arrowstyle="->", color='#273647', lw=2))

plt.title("TraceCrop System Block Diagram", fontsize=16, fontweight='bold', pad=20, color='#051424')
plt.xlim(0, 12)
plt.ylim(1, 3)
plt.tight_layout()
plt.savefig("block_diagram.png", dpi=300, bbox_inches='tight')
plt.close()

# 2. Create PDF using fpdf2
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", 'B', 16)
        self.set_text_color(5, 20, 36)
        self.cell(0, 10, "TraceCrop: Innovation Proposal", 0, 1, 'C')
        self.line(10, 20, 200, 20)
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()

sections = [
    ("1. THEME / SECTOR", "Agriculture Technology (AgriTech), Supply Chain Management, Logistics, and Food Safety."),
    ("2. UNIQUENESS / NEWNESS OF INNOVATION", "TraceCrop provides real-time neural-driven data fusion and immutable tracking using a decentralized cloud infrastructure. Unlike traditional paper-based or siloed digital systems, it features role-based interactive dashboards for farmers, distributors, retailers, and consumers to ensure absolute transparency and prevent data manipulation."),
    ("3. CONCEPT AND OBJECTIVE", "Concept: An unbroken, verifiable chain of custody for agricultural products from farm to table.\n\nObjective: To eliminate blind spots in the supply chain, reduce food spoilage, ensure fair compensation for producers, and provide end-consumers with transparent, scannable insights regarding the origin and journey of their food."),
    ("4. POTENTIAL AREAS OF APPLICATION IN INDUSTRY / MARKET", "- Agricultural cooperatives and farming networks.\n- Food processing and packaging companies.\n- Grocery retail chains and supermarkets.\n- Export/Import logistics and cross-border trade.\n- Pharmaceutical and cold-chain logistics."),
    ("5. MARKET POTENTIAL OF IDEA / INNOVATION", "The global supply chain transparency market is expanding rapidly due to increasing regulatory requirements and consumer demand for ethical sourcing. TraceCrop can be monetized via a SaaS licensing model for enterprise clients, alongside transaction-based fees for mid-market logistics providers. The scalable architecture allows for rapid deployment across emerging markets."),
    ("6. BLOCK DIAGRAM", "")
]

for heading, text in sections:
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(16, 185, 129) # Primary color
    pdf.cell(0, 8, heading, 0, 1)
    
    if text:
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, text)
    pdf.ln(6)

pdf.image("block_diagram.png", x=10, w=190)

output_file = "TraceCrop_Innovation_Proposal.pdf"
pdf.output(output_file)
print(f"Generated {output_file} successfully.")
