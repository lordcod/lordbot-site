function register(event) {
    id = event.id
    var url_oauth = `https://discord.com/oauth2/authorize?guild_id=${id}&scope=bot+applications.commands&client_id=1095713975532007434&permissions=-1`
    window.open(url_oauth, '_blank', 'location=yes,height=570,width=620,scrollbars=yes,status=yes')
};
function dashboard(event) {
    id = event.id
    window.open(`/dashboard/${id}`,'_parent');
};
