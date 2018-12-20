var scroll_widget = document.getElementById("udb_history_scroll");
var num_of_stored_el = 20;

function store(new_entries) {
    strList = sessionStorage.getItem('udb_history');
    var list = []
    if (strList != null)
    {
        list = JSON.parse(strList);
    }
    list = list.concat(new_entries);
    if (list.length > num_of_stored_el)
    {
        list = list.slice(1)
    }
    sessionStorage.setItem('udb_history', JSON.stringify(list));
    return list
}
function removeChildren(dom)
{
    while(dom.firstChild)
    {
        dom.removeChild(dom.firstChild)
    }
}	
function updateScrollWidget(new_entries)
{
    var list = store(new_entries);
    
    removeChildren(scroll_widget)
    for (var i = 0; i < list.length; ++i)
    {
        var entry = document.createElement("li")
        entry.appendChild(document.createTextNode(list[i]))
        entry.classList.add('list-group-item')
        scroll_widget.appendChild(entry)
    }        
    if (new_entries.length != 0)
    {
        scroll_widget.scrollTop = scroll_widget.scrollHeight;
    }
}
updateScrollWidget([])
scroll_widget.scrollTop = scroll_widget.scrollHeight;
