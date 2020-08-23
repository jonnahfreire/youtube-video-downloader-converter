const c = (el) => document.querySelector(el);
const cs = (el) => document.querySelectorAll(el);
let media_format = '';
let video_item = ''
let video_list = []

c('.content-results').scrollIntoView(true);

// DISABLE CONTEXTMENU
window.addEventListener('contextmenu', (e)=>{
	if (e.button == 2){
		e.preventDefault();
		return false;
	}
})

// DISABLE KEY CONTEXTMENU
window.addEventListener('keyup', (e)=>{
	if (e.keyCode === 93){
		e.preventDefault();
		return false;
	}
})

if(c('.search-input').autofocus){
	c('.search').style.boxShadow = "0px 0px 5px #3ec0e8";
}

// SEARCH INPUT
let btn_search = document.querySelector('.search-btn');
let input_search = document.querySelector('.search-input');
let modal = document.querySelector('.modal');

btn_search.addEventListener('mouseover', ()=>{
	c('.search-img').src = 'src/images/search-white.svg';
})

btn_search.addEventListener('mouseout', ()=>{
	c('.search-img').src = 'src/images/search.svg';
})

input_search.addEventListener('focus', ()=>{
	c('.search').style.boxShadow = "0px 0px 5px #3ec0e8";
})

input_search.addEventListener('blur', ()=>{
	c('.search').style.boxShadow = "none";
})


input_search.addEventListener('keyup', ()=>{
	if (input_search.value.length > 5){
		c('.clear-input').style.display = 'flex';
	}else if(input_search.value.length < 5) {
		c('.clear-input').style.display = 'none';
	}
})

c('.clear-input-img').addEventListener('mouseover', ()=>{
	c('.clear-input-img').style.backgroundColor = '#ddd';
});

c('.clear-input-img').addEventListener('mouseout', ()=>{
	c('.clear-input-img').style.backgroundColor = 'white';
});

c('.clear-input-img').addEventListener('click', ()=>{
	input_search.value = '';
	input_search.focus();
	c('.clear-input').style.display = 'none';
});

const video_search = async ()=>{

	modal.style.opacity = 0;
	modal.style.display = 'flex';
	setTimeout(()=>{
		modal.style.opacity = 1;
	}, 50);


	video_info = await eel.search(input_search.value)();
	video_list = [];

	for (item in video_info){
		video_list.push(video_info[item]);
	}

	// REMOVE ALL THE SEARCH ITEMS TO PLACE THE NEW ONES
	cs('.content-results .search-result-items').forEach((item)=>{item.remove()})

	if(input_search.value.length <= 0){
		c('.search-result-p').innerHTML = 'Resultados: ';
		c('.search-result-span').innerHTML = 'Em alta';
	}else{
		c('.search-result-p').innerHTML = `Mostrando ${video_list.length} resultados para: `;
		c('.search-result-span').innerHTML = input_search.value;
	}
	
	setTimeout(()=>{
		modal.style.display = 'none';
		modal.style.opacity = 0;
	}, 2000);

	c('.content-results').scrollTo(0, 0);
	show_search_results();
}


// INPUT SEARCH CLICK
btn_search.addEventListener('click', ()=>{
	video_search();
});

// INPUT SEARCH PRESS ENTER
input_search.addEventListener('keydown', (e)=>{
	if (e.keyCode === 13){
		video_search();
	}
});


const show_search_results = ()=>{
	
	video_list.map((item) => {
		let video_item = c('.content .search-result-items').cloneNode(true);

		video_item.querySelector('.thumbnail').src = item.thumbnail;
		video_item.querySelector('.items .results-title h3').innerHTML = item.title;
		video_item.querySelector('.duration').innerHTML = item.duration;

		video_item.querySelector('.btn-download').addEventListener('click', (e)=>{
			
			let msg_download = video_item.querySelector('.msg-download');
			let msg_download_concluded = video_item.querySelector('.msg-download-concluded');
			let close_msg_concluded = video_item.querySelector('.close-msg-concluded');
			let formats = video_item.querySelector('.formats');

			let format_options = video_item.querySelector('.format-options');
			
			let media_format = format_options.options[format_options.selectedIndex].value

			if(msg_download.style.display === 'none'){
				msg_download_concluded.style.display = 'none';
				msg_download.style.display = 'flex';
				formats.style.display = 'none';

				// CALL THE BACK-END FUNCTION TO DOWNLOAD
				setTimeout(()=>{
					eel.verify(item.url, item.title, media_format);
				}, 2000)

			}else{
				let wait_msg = video_item.querySelector('.wait-msg');
				wait_msg.style.display = 'flex';
				setTimeout(()=>{
					wait_msg.style.display = 'none';	
				}, 3000);
			}
		});

		video_item.addEventListener('mouseover', ()=> {
			setTimeout(()=>{
    			video_item.querySelector('.container-duration').style.opacity=1;
			}, 50);
		});

		video_item.addEventListener('mouseout', ()=> {
			setTimeout(()=>{
    			video_item.querySelector('.container-duration').style.opacity=0;
			}, 50);
		});
	
		// CLOSE MSG CONCLUDED
		video_item.querySelector('.close-msg-concluded').addEventListener('click', ()=>{
			let msg_download_concluded = video_item.querySelector('.msg-download-concluded');
			msg_download_concluded.style.display = 'none';
		});

		
		c('.content-results').appendChild(video_item)
	});
}



window.onload = ()=> {  
    document.onkeydown = function (e) {  
        return (e.which || e.keyCode) != 116;  
    }
    // INITIALIZE SEARCH
	video_search();
	// show_search_results();
}

let menu_item = cs('.menu-item');
let downloader = c('.container-search-result');
let conversor = c('.conversor');
let sobre = c('.sobre');
let div_search = c('.search')

menu_item[0].addEventListener('click', ()=>{
	conversor.style.display = 'none';
	downloader.style.display = 'block';
	sobre.style.display = 'none';
	div_search.style.display = 'flex';
	menu_item[0].classList.add('active');
	menu_item[1].classList.remove('active');
	menu_item[2].classList.remove('active');
});

menu_item[1].addEventListener('click', ()=>{
	conversor.style.display = 'flex';
	downloader.style.display = 'none';
	sobre.style.display = 'none';
	div_search.style.display = 'none';
	menu_item[0].classList.remove('active');
	menu_item[1].classList.add('active');
	menu_item[2].classList.remove('active');
});

menu_item[2].addEventListener('click', ()=>{
	conversor.style.display = 'none';
	downloader.style.display = 'none';
	sobre.style.display = 'flex';
	div_search.style.display = 'none';
	menu_item[0].classList.remove('active');
	menu_item[1].classList.remove('active');
	menu_item[2].classList.add('active');
});


// UNSET DOWNLOAD MESSAGE AND SET DOWNLOAD CONCLUDED MESSAGE
eel.expose(download_concluded)
function download_concluded(video_title){
	// VERIFY IF THE TITLE OF THE FILE DOWNLOADED 
	// RETURNED FROM BACK-END IS EQUAL TO THE ONE 
	// THAT '.msg-download' CLASS STYLE IS SET TO 'flex', 
	// AND UNSETS, SHOWING THAT THE FILE HAS BEEN DOWNLOADED SUCCESSFUL 
	for( i=0; i < c('.content-results').childElementCount; i++ ){
		if ( cs('.content-results .results-title h3')[i].innerText === video_title
			&& cs('.content-results .msg-download')[i].style.display === 'flex'){
			cs('.content-results .msg-download')[i].style.display = 'none';
			cs('.content-results .formats')[i].style.display = 'flex';
			cs('.content-results .msg-download-concluded')[i].style.display = 'flex';
			cs('.content-results .wait-msg')[i].style.display = 'none';
		}
	}
}

eel.expose(msg_error)
function msg_error(video_title){
	for( i=0; i < c('.content-results').childElementCount; i++ ){
		if ( cs('.content-results .results-title h3')[i].innerText === video_title
			&& cs('.content-results .msg-download')[i].style.display === 'flex'){
			setTimeout(()=>{
				cs('.wait-msg')[i].innerHTML = 'Desculpe ocorreu um erro, tente novamente';
			}, 3000)
		}
	}
}
