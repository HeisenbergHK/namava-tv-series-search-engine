const resultList = document.getElementById("result-list");
const inputField = document.getElementById("search-input");

async function fetchData(keyword) {
  const url = `http://127.0.0.1:5000/api/v1/top_match?keyword=${keyword}`;
  const response = await fetch(url);
  const data = await response.json();

  return data;
}

async function logToConsole(keyword) {
  const data = await fetchData(keyword);
  console.log(data);
}

// logToConsole("آخر")

async function renderResults(keyword) {
  const data = await fetchData(keyword);
  console.log(data);
  let resultHTML = "";

  for (let i = 0; i < data.length; i++) {
    // resultHTML += `<div class="result-item">${data[i].series_name}</div>`;
    resultHTML += `<div class="result-item">
                    <img class="poster-el" src="${data[i].series_image_url}" alt="${data[i].series_name}">
                    <span>${data[i].series_name}</span>

                    <div class="rating-div">
                      <div class="star-el">
                        <img class="star-fav" src="images/star.png" alt="star-el" />
                        <span>${data[i].hit}</span>
                      </div>
                      <div class="imdb-el">
                        <img class="imdb-fav" src="images/imdb.png" alt="star-el" />
                        <span>${data[i].imdb}</span>
                      </div>
                    </div>

                  </div>`;
  }

  resultList.innerHTML = resultHTML;

  // console.log(resultHTML);
}

inputField.addEventListener("input", function () {
  const keyword = inputField.value;
  renderResults(keyword);
});

document.addEventListener("DOMContentLoaded", function () {
  resultList.innerHTML = "";
});
