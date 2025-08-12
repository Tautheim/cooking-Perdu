from pathlib import Path
from os import getlogin
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.messagebox import showwarning, askokcancel, showinfo, askyesnocancel
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
from jsonTreatment import read_json, write_json
from variable import thisFilePath
from pdfGenerator import write_document


frameWidth = 800
frameHeight =10
backgroundColor = "#FFFFDD"
foregroundColor = "#CCAACC"
textFont = ("Charlemagne Std", 11, "normal")
labelframeFont = ("Charlemagne Std", 11, "bold")

class gestionnaire_BDD():
    def __init__(self, root:tk.Tk):
        self._variables_()
        self.listVariables = list(self.__dict__.keys())
        self.root = root
        self.root.title("Gestionnaire de recettes")
        self.root.configure(bg=backgroundColor,padx=5, pady=5)
        self.root.resizable(False,False)
        self.frame_introduction().grid(column=0, row=0, columnspan=2, ipady=5)
        self.frame_selectionRecette().grid(column=0, row=1, columnspan=2, sticky="nw", ipady=5)
        self.frame_recipeType().grid(column=0, row=2, columnspan=2, sticky="nw", ipady=5)
        self.frame_times().grid(column=0, row=3, sticky="nw", ipady=5)
        self.frame_ingredients().grid(column=0, row=4, sticky="nw", ipady=5)
        self.frame_picture().grid(column=0, row=5, sticky="nw", ipady=5)
        self.frame_etapes().grid(column=1, row=3, rowspan=3)
        self.frame_button().grid(column=0, row=6, columnspan=2)
    
    def frame_introduction(self)->tk.Frame:
        bgColor = backgroundColor
        frame = tk.Frame(self.root, bg=bgColor, width=frameWidth, height=frameHeight*10)
        frame.grid_propagate(False)
        tk.Label(frame, text="Gestionnaire de recettes".upper(), font=("Arial", 20, "bold"), bg=bgColor, fg=foregroundColor).grid(column=0, row=0)
        textLabel = "Bienvenue dans cette interface de gestion des recettes !\n"+\
            "Ici vous pouvez ajouter, visualiser, modifier ou encore supprimer une recette dans la base de donnée.\n"+\
                "Pour ce faire définissez ou choisissez le nom d'une recette et complétez les champs pour ajouter/modifier une recette."
        tk.Label(frame, text=textLabel, font=textFont, bg=bgColor, justify="left").grid(column=0, row=1, sticky="nw")
        return frame

    def frame_selectionRecette(self)->tk.Frame:
        bgColor = backgroundColor
        frame = tk.Frame(self.root, bg=bgColor, width=frameWidth, height=frameHeight*2)
        frame.grid_propagate(False)
        tk.Label(frame, text="Nom de la recette :", font=textFont, bg=bgColor, width=15, anchor="w").grid(column=0, row=0, sticky="nw")
        self.comboboxNameRecipe = ttk.Combobox(frame, values=self.listRecipes, font=textFont, width=78)
        self.comboboxNameRecipe.bind('<<ComboboxSelected>>', lambda event:self.updating_interface(self.comboboxNameRecipe.get()))
        self.comboboxNameRecipe.grid(column=1, row=0)
        return frame

    def frame_recipeType(self)->tk.LabelFrame:
        bgColor = backgroundColor
        labelframe = tk.LabelFrame(self.root, text="Type de recette :", font=labelframeFont, bg=bgColor, width=frameWidth, height=frameHeight*4, fg=foregroundColor)
        labelframe.grid_propagate(False)
        col = 0
        for texte in ["Entrée", "Plat", "Dessert", "Apéritif", "Boisson"]:
            tk.Radiobutton(labelframe, text=texte, font=textFont, variable=self.typeRecipe, value=texte, width=10, bg=bgColor, justify="left", cursor='hand2').grid(column=col, row=0)
            col=col+1    
        return labelframe

    def frame_times(self)->tk.LabelFrame:
        bgColor=backgroundColor
        entryWidth = 5
        labelframe = tk.LabelFrame(self.root, text="Temps :", font=labelframeFont, bg=bgColor, width=int(frameWidth/2.5), height=int(frameHeight*8.5), fg=foregroundColor)
        line = 0
        for texte in ["Préparation", "Cuisson", "Repos"] :
            tk.Label(labelframe, text=texte + " :", font=textFont, bg=bgColor).grid(column=0, row=line, sticky="nw")
            line+=1
        line = 0
        for variable in [self.preparationTime, self.cookingTime, self.restingTime] :
            tk.Entry(labelframe, textvariable=variable, font=textFont, width=entryWidth, justify="right").grid(column=1, row=line, sticky="nw")
            line+=1
        labelframe.grid_propagate(False)
        line = 0
        self.comboboxTimePreparationUnit = ttk.Combobox(labelframe, values=self.listTimeUnit, font=textFont, width=6, cursor='hand2', state="readonly")
        self.comboboxTimeCookingUnit = ttk.Combobox(labelframe, values=self.listTimeUnit, font=textFont, width=6, cursor='hand2', state="readonly")
        self.comboboxTimeRestingUnit = ttk.Combobox(labelframe, values=self.listTimeUnit, font=textFont, width=6, cursor='hand2', state="readonly")
        self.comboboxTimePreparationUnit.grid(row=0, column=2, padx=5)
        self.comboboxTimeCookingUnit.grid(row=1, column=2, padx=5)
        self.comboboxTimeRestingUnit.grid(row=2, column=2, padx=5)
        return labelframe

    def frame_ingredients(self)->tk.LabelFrame:
        bgColor = backgroundColor
        labelFrame=tk.LabelFrame(self.root, text="Liste des ingrédients :", font=labelframeFont, bg=bgColor, width=int(frameWidth/2.5), height=frameHeight*20, padx=5, fg=foregroundColor)
        tk.Button(labelFrame, text=self.listCommandTableButton[0], command=lambda:self._tableButton_(self.listCommandTableButton[0]), width=10, cursor='hand2', pady=5).grid(column=0, row=0)
        tk.Button(labelFrame, text=self.listCommandTableButton[1], command=lambda:self._tableButton_(self.listCommandTableButton[1]), width=10, cursor='hand2', pady=5).grid(column=1, row=0)
        tk.Button(labelFrame, text=self.listCommandTableButton[-1], command=lambda:self._tableButton_(self.listCommandTableButton[-1]), width=10, cursor='hand2', pady=5).grid(column=2, row=0)
        listColumns = ["Quantité", "Unité", "Ingrédient"]
        self.treeviewIngredients = ttk.Treeview(labelFrame, columns=listColumns, displaycolumns=listColumns, height=5)
        self.treeviewIngredients.column("#0", width=0, minwidth=0, stretch=False)
        for entete in listColumns :
            self.treeviewIngredients.column(entete, width=100, minwidth=100, anchor="e", stretch=False)
            self.treeviewIngredients.heading(entete, text=entete, anchor="center")
        self.treeviewIngredients.grid(column=0, row=1, columnspan=len(self.listCommandTableButton), ipady=5)
        self.treeviewIngredients.bind("<Button-1>", self._treeview_edit_cell_)
        labelFrame.grid_propagate(False)
        return labelFrame

    def frame_etapes(self)->tk.LabelFrame:
        bgColor=backgroundColor
        labelframe = tk.LabelFrame(self.root, text="Étapes de préparation :", font=labelframeFont, bg=bgColor, width=int(frameWidth/1.7), height=frameHeight*48, padx=5, fg=foregroundColor)
        tk.Entry(labelframe, textvariable=self.cookingStep, font=textFont, width=int(frameWidth/14.5)).grid(column=0, row=0, columnspan=4)
        self.listBoxCookingSteps=tk.Listbox(labelframe, font=textFont, selectmode=tk.SINGLE, width=56, height=int(frameHeight*2.2))
        self.listBoxCookingSteps.grid(column=0, row=2, columnspan=4)
        tk.Button(labelframe, text="Ajouter", command=lambda:self._listboxButton_("Ajouter"), cursor="hand2", width=10).grid(column=0, row=1)
        tk.Button(labelframe, text="Insérer avant", command=lambda:self._listboxButton_("Insérer"), cursor="hand2", width=10).grid(column=1, row=1)
        tk.Button(labelframe, text="Modifier", command=lambda:self._listboxButton_("Modifier"), cursor="hand2", width=10).grid(column=2, row=1)
        tk.Button(labelframe, text="Supprimer", command=lambda:self._listboxButton_("Supprimer"), cursor="hand2", width=10).grid(column=3, row=1)
        labelframe.grid_propagate(False)
        return labelframe

    def frame_picture(self)->tk.LabelFrame:
        bgColor = backgroundColor
        labelFrame = tk.LabelFrame(self.root, text="Image du plat :", font=labelframeFont, width=int(frameWidth/2.5), height=frameHeight*17, fg=foregroundColor, bg=bgColor, padx=5)
        tk.Entry(labelFrame, textvariable=self.pictureName, width=int(frameWidth/17)).grid(column=0, row=0)
        tk.Button(labelFrame, text="...", command=self._pictureButton_).grid(column=1, row=0)
        self.canvasPicture = tk.Canvas(labelFrame, width=int(frameWidth/2.7), height=int(frameHeight*12.5), bg=bgColor, highlightthickness=0, bd=0)
        self.canvasPicture.grid(column=0, row=1, columnspan=2)
        labelFrame.grid_propagate(False)
        return labelFrame

    def frame_button(self)->tk.Frame:
        bgColor = backgroundColor
        buttonWidth = 17
        frame = tk.Frame(self.root, width=frameWidth, height=frameHeight*4, bg=bgColor, pady=5)
        tk.Button(frame, text="Nouvelle recette", command=lambda:self.updating_interface(""), cursor="hand2", width=buttonWidth).grid(column=0, row=0)
        tk.Button(frame, text="Enregistrer recette", command=self.saving_recipe, cursor="hand2", width=buttonWidth).grid(column=1, row=0)
        tk.Button(frame, text="Annuler modifications", command=lambda:self.updating_interface(self.comboboxNameRecipe.get()), cursor="hand2", width=buttonWidth).grid(column=2, row=0)
        tk.Button(frame, text="Supprimer recette", command=self.deleting_recipe, cursor="hand2", width=buttonWidth).grid(column=3, row=0)
        tk.Button(frame, text="Générer le pdf", command=self.generating_pdf, cursor="hand2", width=buttonWidth).grid(column=4, row=0)
        tk.Button(frame, text="Mette en ligne", command=None, cursor="hand2", width=buttonWidth).grid(column=5, row=0)
        frame.grid_propagate(False)
        return frame

    def _variables_(self):
        self.recipesData = read_json()
        self.comboboxNameRecipe: ttk.Combobox
        self.comboboxTimePreparationUnit: ttk.Combobox
        self.comboboxTimeCookingUnit: ttk.Combobox
        self.comboboxTimeRestingUnit: ttk.Combobox
        self.treeviewIngredients: ttk.Treeview
        self.listBoxCookingSteps: tk.Listbox
        self.canvasPicture: tk.Label
        self.picture: Image
        self.listSteps:list = []
        self.listRecipes: list = [name for name in self.recipesData.keys()]
        self.listTimeUnit: list = ["s", "min", "h", 'jour(s)']
        self.listCommandTableButton: list = ["Ajouter", "Supprimer", "Vider"]
        self.recipeName: tk.StringVar = tk.StringVar()
        self.typeRecipe: tk.StringVar = tk.StringVar()
        self.typeRecipe.set(None)
        self.preparationTime: tk.IntVar = tk.IntVar()
        self.cookingTime: tk.IntVar = tk.IntVar()
        self.restingTime: tk.IntVar = tk.IntVar()
        self.cookingStep: tk.StringVar = tk.StringVar()
        self.pictureName: tk.StringVar = tk.StringVar()

    def updating_interface(self, recipeName:str=""):
        self._tableButton_("Vider")
        self._listboxButton_("Vider")
        self.comboboxTimeCookingUnit.set("")
        self.comboboxTimePreparationUnit.set("")
        self.comboboxTimeRestingUnit.set("")
        self.recipesData = read_json()
        if recipeName == "":
            self.comboboxNameRecipe.set("")
            for variableName in self.listVariables:
                if variableName != "listTimeUnit" and variableName != "listCommandTableButton" :
                    variable = self.__dict__[variableName]
                    if variableName == "typeRecipe" : variable.set(None)
                    elif variableName=="listRecipes" :
                        self.comboboxNameRecipe["values"] = [name for name in self.recipesData.keys()]
                    else :
                        if type(variable) == tk.StringVar : variable.set("")
                        elif type(variable) == tk.IntVar : variable.set(0)
                        elif type(variable) == list : variable = []
        elif recipeName in self.recipesData.keys() :
            recipeData = self.recipesData[recipeName]
            self.typeRecipe.set(recipeData["Type"])
            self.cookingTime.set(recipeData["Temps"]["Cuisson"][0])
            self.comboboxTimeCookingUnit.set(recipeData["Temps"]["Cuisson"][-1])
            self.preparationTime.set(recipeData["Temps"]["Préparation"][0])
            self.comboboxTimePreparationUnit.set(recipeData["Temps"]["Préparation"][-1])
            self.restingTime.set(recipeData["Temps"]["Repos"][0])
            self.comboboxTimeRestingUnit.set(recipeData["Temps"]["Repos"][-1])
            for ingredient in recipeData["Ingrédients"]:
                self.treeviewIngredients.insert("", "end", values=ingredient)
            for preparation in recipeData["Préparation"] :
                self.listBoxCookingSteps.insert(tk.END, preparation)

    def saving_recipe(self):
        Nom = self.comboboxNameRecipe.get()
        saving = False
        if Nom in self.listRecipes :
            answer = askokcancel(title="Attention", message="Cette recette existe déjà, voulez-vous la remplacer ?")
            if answer == True: saving = True
            else : saving = False
        else : saving = True
        if saving == True :
            self.recipesData[Nom] = {"Type":self.typeRecipe.get()}
            Time = {"Préparation":[self.preparationTime.get(), self.comboboxTimePreparationUnit.get()],\
                    "Cuisson":[self.cookingTime.get(), self.comboboxTimeCookingUnit.get()],\
                    "Repos":[self.restingTime.get(), self.comboboxTimeRestingUnit.get()]}
            self.recipesData[Nom]["Temps"] = Time.copy()
            Ingr = []
            for item_id in self.treeviewIngredients.get_children():
                valeurs = self.treeviewIngredients.item(item_id, "values")
                Ingr.append([valeurs[0], valeurs[1], valeurs[-1]])
            self.recipesData[Nom]["Ingrédients"] = Ingr.copy()
            self.recipesData[Nom]["Préparation"] = [step for step in self.listBoxCookingSteps.get(0, tk.END)]
            write_json(self.recipesData)
            showinfo(title="Sauvegarde", message=f'La recette "{Nom}" a été sauvegardée avec succès.')
            self.updating_interface()
        return

    def deleting_recipe(self):
        Nom = self.comboboxNameRecipe.get()
        answer = askokcancel(title="Supression", message=f"Voulez-vous vraiment supprimer la recette \"{Nom}\" de la base de données ?")
        if answer == True :
            del(self.recipesData[Nom])
            write_json(self.recipesData)
            self.updating_interface()
        else :
            pass
        return

    def generating_pdf(self):
        Nom = self.comboboxNameRecipe.get()
        if Nom !="":
            answer = askyesnocancel(title="Générateur pdf", message=f"Voulez-vous enregistrer la recette \"{Nom}\" avant de générer le pdf ?")
            if answer == True: self.saving_recipe()
            elif answer == None: return
        self.recipesData = read_json()
        write_document(self.recipesData)
        showinfo(title="Générateur pdf", message="Le pdf a été généré avec succès.")

    def _tableButton_(self, value:str):
        if value == self.listCommandTableButton[0]:
            self.treeviewIngredients.insert("","end", values=(0,"","Nom"))
        elif value == self.listCommandTableButton[1]:
            selected = self.treeviewIngredients.selection()
            for item in selected:
                self.treeviewIngredients.delete(item)
        elif value == self.listCommandTableButton[-1]:
            for item in self.treeviewIngredients.get_children():
                self.treeviewIngredients.delete(item)
        return

    def _listboxButton_(self, value:str):
        texte = self.cookingStep.get()
        if value == "Ajouter":
            if texte != "" : self.listBoxCookingSteps.insert(tk.END, texte)
        elif value == "Insérer":
            if texte != "" : 
                select = self.listBoxCookingSteps.curselection()
                if select == () :
                    showwarning("Sélection invalide", message="Veuillez sélectionner une ligne à modifier.")
                else :
                    self.listBoxCookingSteps.insert(select, texte)
        elif value == "Modifier":
            if texte != "" : 
                select = self.listBoxCookingSteps.curselection()
                if select == () :
                    showwarning("Sélection invalide", message="Veuillez sélectionner une ligne à modifier.")
                else :
                    self.listBoxCookingSteps.delete(select)
                    self.listBoxCookingSteps.insert(select, texte)
        elif value == "Supprimer":
            select = self.listBoxCookingSteps.curselection()
            if select == () :
                showwarning("Sélection invalide", message="Veuillez sélectionner une ligne à supprimer.")
            else :
                self.listBoxCookingSteps.delete(select)
        elif value == "Vider":
                self.listBoxCookingSteps.delete(0, tk.END)
        self.cookingStep.set("")
        return

    def _pictureButton_(self):
        path = askopenfilename(title="Image", initialdir=Path("C:/Users",getlogin(), "Pictures"), filetypes=[('png', '.png'),('jpeg','.jpeg'),('jpg','.jpg'), ('all', '*')])
        self.pictureName.set(path)
        self.picture = Image.open(path)
        imgWidth, imgHeight = self.picture.size
        ratio = imgWidth/imgHeight
        canvasWidth, canvasHeight = self.canvasPicture.winfo_width(), self.canvasPicture.winfo_height()
        self.picture = self.picture.resize((int(ratio*canvasHeight), int(canvasHeight)), Image.LANCZOS)
        img = ImageTk.PhotoImage(self.picture)
        self.canvasPicture.create_image(int(canvasWidth/2), int(canvasHeight/2), anchor='center', image=img)

    def _treeview_edit_cell_(self, event):
        if hasattr(self, "_active_entry") and self._active_entry:
            self._treeview_save_edit_()

        region = self.treeviewIngredients.identify_region(event.x, event.y)
        if region != "cell":
            return

        selected_item = self.treeviewIngredients.focus()
        if not selected_item:
            return

        col = self.treeviewIngredients.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1

        bbox = self.treeviewIngredients.bbox(selected_item, col)
        if not bbox:
            return

        x, y, width, height = bbox
        value = self.treeviewIngredients.item(selected_item, "values")[col_index]

        entry = tk.Entry(self.treeviewIngredients)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        self._active_entry = entry
        self._active_item = selected_item
        self._active_col_index = col_index

        entry.bind("<Return>", lambda e: self._treeview_save_edit_())
        entry.bind("<Escape>", lambda e: self._treeview_cancel_edit_())

    def _treeview_save_edit_(self):
        if not hasattr(self, "_active_entry") or not self._active_entry:
            return
        new_value = self._active_entry.get()
        values = list(self.treeviewIngredients.item(self._active_item, "values"))
        values[self._active_col_index] = new_value
        self.treeviewIngredients.item(self._active_item, values=values)
        self._active_entry.destroy()
        self._active_entry = None

    def _treeview_cancel_edit_(self):
        if hasattr(self, "_active_entry") and self._active_entry:
            self._active_entry.destroy()
            self._active_entry = None



if __name__ == "__main__" :
    root = tk.Tk()
    gestionnaire_BDD(root=root)
    root.mainloop()