// # Author: Jude Maggitti
// # Last Modified: 3/10/24
// # Summary: gets the list of articles in html form
function fetchArticleListData() {
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function () {
        const abArr = JSON.parse(this.responseText);

        const article_List = document.getElementById("article_List");

        article_List.innerHTML = '';

        Object.keys(abArr).forEach(function (item) {
            const articleListItem = document.createElement("ul");
            articleListItem.innerHTML = `
            <li>
             <a href = "/html/Version1/Article.html?key=${encodeURIComponent(item)}" class="custom-link" ><p class = "medium font">${item}</p></a>
           </form>
         </li>
            `;
            article_List.appendChild(articleListItem);
        });
    };
    xmlhttp.open("GET", "/static/json/AuthorSample.json", true);//gets json file
    xmlhttp.send();
}
document.addEventListener("DOMContentLoaded", function () {
    fetchArticleListData();
});
