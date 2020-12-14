async function getData () {
	var xhr = new XMLHttpRequest();
	
	host = window.location.host
	path = document.getElementById("hostname").getAttribute('href')
	var url = 'http://' + host + path
	
    xhr.open("GET", url, false);
    xhr.send();
    var data= JSON.parse(xhr.responseText);
    return data
}

const list_element = document.getElementById('posts');
const pagination_element = document.getElementById('pagenumbers');

let current_page = 1;
let rows = 5;

function DisplayList (items, wrapper, rows_per_page, page) {
	wrapper.innerHTML = "";
	page--;
	let start = rows_per_page * page;
	let end = start + rows_per_page;
	
	let paginatedItems = items.slice(start, end);

	for (let i = 0; i < paginatedItems.length; i++) {
		let item = paginatedItems[i];

		let item_post = document.createElement('div');
		item_post.classList.add('post');

		let item_post_author = document.createElement('div');
		item_post_author.classList.add('post-author');
		let item_post_author_text = document.createElement('p');
		item_post_author_text.innerHTML = item['author']
		item_post_author.appendChild(item_post_author_text);

		let item_post_title = document.createElement('div');
		item_post_title.classList.add('post-title');
		let item_post_title_text = document.createElement('p');
		item_post_title_text.innerHTML = item.title
		item_post_title.appendChild(item_post_title_text);
		
		let item_post_likes = document.createElement('div');
		item_post_likes.classList.add('post-likes');
		let item_post_likes_text = document.createElement('p');
		item_post_likes_text.innerHTML = item.likes
		item_post_likes.appendChild(item_post_likes_text);

		let item_post_dislikes = document.createElement('div');
		item_post_dislikes.classList.add('post-dislikes');
		let item_post_dislikes_text = document.createElement('p');
		item_post_dislikes_text.innerHTML = item.dislikes
		item_post_dislikes.appendChild(item_post_dislikes_text);

		let item_post_link = document.createElement('div');
		item_post_link.classList.add('post-link');
		let item_post_link_a = document.createElement('a');
		item_post_link_a.classList.add('post-link-a');
		
		//item_post_link_a.href = "{{ url_for('post_template', post_id=" + item.id + ") }}";

		//a = "{{ url_for('comment_post', post_id="
		//b = item.id
		//c = ") }}"
		//var item_url = a + b + c
		//item_post_link_a.setAttribute("href", host + '/post/' + item.id);

		//item_post_link_a.href = "{{ url_for('post_template', post_id=REPLACE) }}".replace('REPLACE', item.id);

		item_post_link_a.href = flask_util.url_for('post_template', {post_id:item.id});


		item_post_link.appendChild(item_post_link_a);
		let item_post_link_text = document.createElement('p');
		item_post_link_text.classList.add('post-link-text');
		item_post_link_text.innerHTML = "Check it out!"
		item_post_link_a.appendChild(item_post_link_text);

		item_post.appendChild(item_post_author);
		item_post.appendChild(item_post_title);
		item_post.appendChild(item_post_likes);
		item_post.appendChild(item_post_dislikes);
		item_post.appendChild(item_post_link);

		wrapper.appendChild(item_post);
	}
}

function SetupPagination (items, wrapper, rows_per_page) {
	wrapper.innerHTML = "";

	let page_count = Math.ceil(items.length / rows_per_page);
	for (let i = 1; i < page_count + 1; i++) {
		let btn = PaginationButton(i, items);
		wrapper.appendChild(btn);
	}
}

function PaginationButton (page, items) {
	let button = document.createElement('button');
	button.innerText = page;

	if (current_page == page) button.classList.add('active');

	button.addEventListener('click', function () {
		current_page = page;
		DisplayList(items, list_element, rows, current_page);

		let current_btn = document.querySelector('.pagenumbers button.active');
		current_btn.classList.remove('active');

		button.classList.add('active');
	});

	return button;
}

var data = getData().then(list_items => {
    DisplayList(list_items, list_element, rows, current_page);
    SetupPagination(list_items, pagination_element, rows);
})





















