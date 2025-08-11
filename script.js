var recipesURL = "recettes.json";
let recettes = {};

async function chargerRecettes() {
    const response = await fetch(recipesURL);
    if (!response.ok) {
        throw new Error("Erreur de chargement JSON");
    }
    return await response.json();
}

function getSelectedTypesRecipe() {
    const checkedBoxes = document.querySelectorAll('input[name="typeRecipe[]"]:checked');
    return Array.from(checkedBoxes).map(cb => cb.value);
}

function majListboxRecettes(data) {
    const select = document.getElementById("listRecipes");
    select.innerHTML = "";

    const filters = getSelectedTypesRecipe();
    const recherche = document.getElementById("recipeResearch").value.toLowerCase();

    Object.keys(data).forEach(recipeName => {
        const recipeType = data[recipeName].Type;
        const matchType = filters.includes(recipeType);
        const matchRecherche = recipeName.toLowerCase().includes(recherche);

        if (matchType && matchRecherche) {
            const option = document.createElement("option");
            option.value = recipeName;
            option.textContent = recipeName;
            select.appendChild(option);
        }
    });
}

function afficherRecetteDetails(recipeName) {
    const recette = recettes[recipeName];
    if (!recette) return; // sécurité si recette non trouvée
    document.querySelector(".dataRecipe").hidden = false;

    // Nom
    document.querySelector(".recipeName").textContent = recipeName;

    // Type
    document.getElementById("Type").textContent = recette.Type;

    // Temps
    document.getElementById("preparingTimeValue").textContent = recette.Temps.Préparation[0];
    document.getElementById("preparingTimeUnit").textContent = recette.Temps.Préparation[1];

    document.getElementById("restingTimeValue").textContent = recette.Temps.Repos[0];
    document.getElementById("restaringTimeUnit").textContent = recette.Temps.Repos[1];

    document.getElementById("cookingTimeValue").textContent = recette.Temps.Cuisson[0];
    document.getElementById("cookingTimeUnit").textContent = recette.Temps.Cuisson[1];

    // Ingrédients (liste)
    const containerIngredients = document.getElementById("recipeIngredient");
    containerIngredients.innerHTML = "<legend><b>Ingrédients :</b></legend>"; // reset

    const ulIngredients = document.createElement("ul");
    recette.Ingrédients.forEach(ing => {
        // ing = [quantité, unité, nom]
        const li = document.createElement("li");
        li.textContent = `${ing[0]} ${ing[1]} ${ing[2]}`.trim();
        ulIngredients.appendChild(li);
    });
    containerIngredients.appendChild(ulIngredients);

    // Étapes de préparation (liste)
    const containerSteps = document.getElementById("recipeSteps");
    containerSteps.innerHTML = "<legend><b>Étapes de préparation :</b></legend>"; // reset

    const olSteps = document.createElement("ol");
    recette.Préparation.forEach(step => {
        const li = document.createElement("li");
        li.textContent = step;
        olSteps.appendChild(li);
    });
    containerSteps.appendChild(olSteps);
}

function initialiserEvenements() {
    // Écoute sur les cases à cocher
    document.querySelectorAll('input[name="typeRecipe[]"]').forEach(cb => {
        cb.addEventListener("change", () => majListboxRecettes(recettes));
    });

    // Écoute sur la barre de recherche
    document.getElementById("recipeResearch").addEventListener("input", () => {
        majListboxRecettes(recettes);
    });

    //Écoute sur la sélection de recette
    document.getElementById("listRecipes").addEventListener("change", (event)=>{
        afficherRecetteDetails(event.target.value)
    })
}

function startApp() {
    chargerRecettes().then(data => {
        recettes = data;
        majListboxRecettes(recettes); // Affiche les recettes au chargement
        initialiserEvenements();       // Configure les événements après chargement des données
    });
}

startApp();