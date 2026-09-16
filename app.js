(function(){
const dialog=document.querySelector('#player');
const video=document.querySelector('#video');
const charLabel=document.querySelector('#current-char');
const wordLabel=document.querySelector('#current-word');
const download=document.querySelector('#dialog-download');
function stop(){video.pause();video.currentTime=0;}
function start(){const played=video.play();if(played&&played.catch)played.catch(function(){});}
function open(button){
  stop();
  const src=button.dataset.video;const char=button.dataset.char;
  charLabel.textContent=char;
  wordLabel.textContent=button.dataset.word||'';
  video.src=src;
  download.href=src;
  download.setAttribute('download',char+'字彩色筆順動畫.mp4');
  if(!dialog.open)dialog.showModal();
  start();
}
document.addEventListener('click',function(event){
  const target=event.target.closest&&event.target.closest('[data-video]');
  if(target)open(target);
});
document.querySelector('#replay').addEventListener('click',function(){video.currentTime=0;start();});
document.querySelector('#close').addEventListener('click',function(){dialog.close();});
dialog.addEventListener('click',function(event){if(event.target===dialog)dialog.close();});
dialog.addEventListener('close',stop);
})();