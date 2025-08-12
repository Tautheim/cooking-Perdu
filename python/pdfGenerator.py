import typing
from jsonTreatment import read_json

from reportlab.lib.pagesizes import A4 as A4_size
from reportlab.platypus import BaseDocTemplate, Paragraph, PageBreak, Frame, PageTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import PageBreak
from reportlab.platypus.tableofcontents import TableOfContents


A4_width, A4_height = A4_size

document = BaseDocTemplate(
    "Recettes-cuisines.pdf",
    pagesize=A4_size,
    leftMargin=50,
    rightMargin=50,
    topMargin=60,
    bottomMargin=60
)

frame = Frame(
    document.leftMargin,
    document.bottomMargin,
    document.width,
    document.height,
    id='normal'
)
template = PageTemplate(id='RecettePage', frames=frame)
document.addPageTemplates([template])

style_recipeName = ParagraphStyle(
    name='Title',
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=18,               # Espacement entre les lignes
    textColor=colors.black,
    alignment=1,              # 0=left, 1=center, 2=right, 4=justified
    spaceBefore=12,
    spaceAfter=12,
    leftIndent=20,
    rightIndent=20,
    backColor=colors.white
)

style_parts = ParagraphStyle(
    name='Parts',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,               # Espacement entre les lignes
    textColor=colors.black,
    alignment=0,              # 0=left, 1=center, 2=right, 4=justified
    spaceBefore=12,
    spaceAfter=5,
    leftIndent=20,
    rightIndent=20,
    backColor=colors.white
)

style_text = ParagraphStyle(
    name='Text',
    fontName='Helvetica',
    fontSize=10,
    leading=13,
    textColor=colors.black,
    alignment=4,
    spaceBefore=0,
    spaceAfter=0,
    leftIndent=20,
    rightIndent=20,
    backColor=colors.white
)

recipes = read_json()
listRecipes = sorted([recipe for recipe in recipes.keys()])
pdfContent = []
tableOfContent = TableOfContents()
tableOfContent.levelStyles = [style_recipeName]

def write_recipes(recipeName:str, data:dict=recipes):
    bookmark = recipeName.replace(" ", "_")
    title = Paragraph(f'<a name="{bookmark}"/>{recipeName.upper()}', style_recipeName)
    pdfContent.append(title)
    document.notify('TOCEntry', (0, recipeName, bookmark))
    recipe_data = recipes[recipeName]
    for partName in recipe_data.keys() :
        writeRecipeParts = Paragraph(partName + " :", style_parts)
        pdfContent.append(writeRecipeParts)
        if partName == "Type":
            writeRecipeType = Paragraph(recipe_data[partName], style_text)
            pdfContent.append(writeRecipeType)
        elif partName == "Temps":
            for timeName in recipe_data[partName].keys():
                writeRecipeTime = Paragraph(f"\t{timeName} : { recipe_data[partName][timeName][0]} { recipe_data[partName][timeName][-1]}", style_text)
                pdfContent.append(writeRecipeTime)
        elif partName == "Ingrédients":
            ingredientData = recipe_data[partName]
            for i in range(len(ingredientData)):
                writeRecipeText = Paragraph(f"\t{ingredientData[i][0]}{ingredientData[i][1]} {ingredientData[i][2]}", style_text)
                pdfContent.append(writeRecipeText)
        elif partName == "Préparation" :
            for i in range(len(recipe_data[partName])):
                writeRecipeText = Paragraph(f"{i+1}.\t{recipe_data[partName][i]}", style_text)
                pdfContent.append(writeRecipeText)
    pdfContent.append(PageBreak())
    

def write_document(data:dict=recipes):
    for Nom in [name for name in data.keys()]:
        write_recipes(Nom, data)
    document.build(pdfContent)

if __name__ == "__main__" :
    write_document()
    