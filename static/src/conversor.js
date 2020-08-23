const select = (el)=>document.querySelector(el);
const selectAll = (el)=>document.querySelectorAll(el);

video_input   = select('.video-input');
btn_converter = select('.btn_converter');
msg_convert	  = select('.msg-convert');
close_msg_concluded  = select('.close-msg-concluded-cv');

modal_cv  = select('.modal-cv');
btn_ok 	  = select('.ok');
msg_error = select('.msg-error p');
msg_popup = select('.msg-popup');

//Select the video file
let file_to_convert = '';

video_input.addEventListener('click', async ()=>{
	if (video_input.value.length  === 0){
		file_name = await eel.open_file_name()();
		video_input.value = file_name;
		file_to_convert = file_name;
	}
})


// Select path to save file
file_path = document.querySelector('.cv-path');

let path_to_save_file = '';

file_path.addEventListener('click', async ()=>{
	if (file_path.value.length  === 0){
		file = await eel.open_file_path()();
		file_path.value = file;
		path_to_save_file = file_path.value;
	}
})

let absolute_path = '';

eel.expose(cv_loader_stop);
function cv_loader_stop() {
	video_input.value = '';
	path_to_save_file = '';
	file_path.value = '';
	absolute_path = '';
	msg_convert.style.display = 'none';
	select('.msg-convert-concluded').style.display = 'flex'
}


btn_converter.addEventListener('click', ()=>{
	
	if (video_input.value.length === 0) {
		modal_cv.style.opacity = 0;
		modal_cv.style.display = 'flex';
		msg_error.innerHTML = 'Por favor selecione um video!';
		setTimeout(()=>{
			modal_cv.style.opacity = 1;
		}, 200);
	}else {
		if(path_to_save_file === ''){
			absolute_path = file_to_convert.slice(0, file_to_convert.lastIndexOf('/')+1);
		}
		console.log(absolute_path, file_to_convert, path_to_save_file)
		msg_convert.style.display = 'flex';
		eel.converter_params(absolute_path, file_to_convert, path_to_save_file);
	}
})


btn_ok.addEventListener('click', ()=>{
	if (modal_cv.style.display === 'flex'){
		modal_cv.style.opacity = 0;
		setTimeout(()=>{
			modal_cv.style.display = 'none';
		}, 200);
	}
})

close_msg_concluded.addEventListener('click', ()=>{
	if (select('.msg-convert-concluded').style.display === 'flex'){
		select('.msg-convert-concluded').style.display = 'none';
	}
})
