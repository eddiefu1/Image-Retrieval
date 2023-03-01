let distance_span = document.getElementById("distance");
let reslutsDiv = document.getElementById("search-results");
let objectsDiv = document.getElementById("img-objects");

window.addEventListener("load", (event) => {
  let inputImage = document.getElementById("input-img");

  loadImageObjects(inputImage);
});

async function loadImageObjects(inputImage) {
  let base = basename(inputImage.src, "/");
  let filename = base.substr(0, base.lastIndexOf(".")).slice(-2);

  let results = [];
  const data = await getJSON();

  data.forEach((item) => {
    image_id = item.id.slice(0, 2);

    if (image_id === filename) {
      results.push(item);
    }
  });

  str = "";
  for (i = 0; i < results.length; i++) {
    str += `<div class="object">
              <img
                id=${results[i].id}
                src=${results[i].image_path}
                alt="No image found"
                class="result-image"
                onclick="changeObject(this)"
              />
            </div>`;
  }

  objectsDiv.innerHTML = "";
  objectsDiv.innerHTML = str;

  let objectsDivChildren = document.getElementById("img-objects").children;
  changeObject(objectsDivChildren[0].children[0]);
}

function changeResult(e) {
  let resultsDivChildren = document.getElementById("search-results").children;
  let result_img = document.getElementById("result-img");

  base = basename(e.src, "/");
  filename = base.substr(0, base.lastIndexOf("."));

  result_img.src = e.src;
  distance_span.innerText = e.id;

  for (i = 0; i < resultsDivChildren.length; i++) {
    resultsDivChildren[i].classList.remove("active-image");
  }

  e.parentElement.classList.add("active-image");
}

function changeObject(e) {
  updateSearchResults(e.id);

  let objectsDivChildren = document.getElementById("img-objects").children;
  let object_img = document.getElementById("object-img");

  base = basename(e.src, "/");
  filename = base.substr(0, base.lastIndexOf("."));

  object_img.src = e.src;

  for (i = 0; i < objectsDivChildren.length; i++) {
    objectsDivChildren[i].classList.remove("active-image");
  }

  e.parentElement.classList.add("active-image");
}

async function updateSearchResults(id) {
  const searchResults = await search(id);

  str = "";

  searchResults.sort((a, b) => (a.dist < b.dist ? 1 : -1));

  for (i = 0; i < searchResults.length; i++) {
    str += `<div class="results">
              <img
                id=${searchResults[i].dist}
                src=${searchResults[i].image_path}
                alt="No image found"
                class="result-image"
                onclick="changeResult(this)"
              />
            </div>`;
  }

  reslutsDiv.innerHTML = "";
  reslutsDiv.innerHTML = str;

  let resultsDivChildren = document.getElementById("search-results").children;
  changeResult(resultsDivChildren[0].children[0]);
}

async function search(id) {
  results = [];
  const data = await getJSON();

  objectFeature = null;
  data.forEach((item) => {
    if (item.id === id) objectFeature = item.feature;
  });

  data.forEach((item) => {
    if (histogramIntersection(objectFeature, item.feature) > 0.9) {
      item.dist = histogramIntersection(objectFeature, item.feature);
      results.push(item);
    }
  });

  return results;
}

async function getJSON() {
  return fetch("http://localhost:3000/data")
    .then((response) => response.json())
    .then((data) => data);
}

function histogramIntersection(a, b) {
  numerator = 0;
  denominator = 0;

  for (i = 0; i < a.length; i++) {
    numerator += minimum(a[i], b[i]);
    denominator += b[i];
  }

  return numerator / denominator;
}

function minimum(a, b) {
  result = 0;
  a <= b ? (result = a) : (result = b);
  return result;
}

function basename(str, sep) {
  return str.substr(str.lastIndexOf(sep) + 1);
}
