// let search = document.querySelector('#search');
// let clear = document.querySelector('#clear');
// let items = document.querySelectorAll('.servers div a div div h1.server-name');
// let notFound = document.querySelector('#notFound');
// let servers = document.querySelector('#serversList');
// search.oninput = () => {
//     let val = search.value.trim().toLowerCase();
//     if (val != ''){
//         clear.classList.remove('hideF')
//         items.forEach((elem) => {

//             if (elem.innerText.toLowerCase().search(val) != -1){
//                 elem.closest('.page-server').classList.remove('hide')
//                 servers.classList.remove('hide')
//                 notFound.classList.remove('hideA')
//                 let hide = document.querySelectorAll('.servers div .hide').length;
//                 if (!(hide == items.length)){
//                     servers.classList.remove('hide')
//                     notFound.classList.add('hide')
//                 }
//             } else {         
//                 elem.closest('.page-server').classList.add('hide')
//                 let hide = document.querySelectorAll('.servers div .hide').length;
//                 if (hide == items.length){
//                     servers.classList.add('hide')
//                     notFound.classList.remove('hide')
//                 }
//             }
//         })
//     } else {
//         items.forEach((elem) => {
//             clear.classList.add('hideF')
//             elem.closest('.page-server').classList.remove('hide')
//             servers.classList.remove('hide')
//             notFound.classList.add('hide')
//         });
//     }
// }

// clear.onclick = () => {
//     search.value = '';
//     items.forEach((elem) => {
//         clear.classList.add('hideF')
//         elem.closest('.page-server').classList.remove('hide')
//     });
// }


function register(event) {
    id = event.id
    var url_oauth = `https://discord.com/oauth2/authorize?guild_id=${id}&scope=bot+applications.commands&client_id=1095713975532007434&permissions=-1`
    window.open(url_oauth, '_blank', 'location=yes,height=570,width=620,scrollbars=yes,status=yes')
};
function dashboard(event) {
    id = event.id
    window.open(`/dashboard/${id}`,'_parent');
};

window.addEventListener('load', function() {
    var page_servers = this.document.getElementsByClassName("page-server")
    for (let key_page in page_servers) {
        let page = page_servers[key_page]
        console.log(page)
        
        let server_name = page.getElementsByClassName("server-name")[0].innerHTML
        let server_avatart_back = page.getElementsByClassName("serever-avatar-back-blur")[0]
        let server_avatar_ico = page.getElementsByClassName("server-avatar-ico")[0]
        
        let avatar_hash = server_avatart_back.getAttribute("hash")
        if  (avatar_hash==="None") {
            let NoneImg = document.createElement("div");
            NoneImg.className = "server-avatar-let"
            NoneImg.innerHTML = server_name.substring(0,1)
            server_avatar_ico.parentNode.replaceChild(NoneImg,server_avatar_ico);
        }
        else {
            let avatar = `https://cdn.discordapp.com/icons/${page.id}/${avatar_hash}.webp?size=240`
            server_avatart_back.style.background = `url(${avatar})`
            server_avatar_ico.src = avatar
        }
        
    }
});