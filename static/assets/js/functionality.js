let count= 2
function add_command(){
    if(count <= 8){
        let id = "cmd_"+count;
        html = '<div class="table-responsive">'
        html +='<table class="table">'
        html +='    <thead>'
        html +='    <tr>'
        html +='        <th id="command_name">Command '+count+ '</th>'
        html +='        <th>&nbsp;Wait</th>'
        html +='    </tr>'
        html +='    </thead>'
        html +='    <tbody>'
        html +='    <tr>'
        html +='        <td>'
        html +='            <input type="text" style="width: 100%;border-radius: 5px;" placeholder="write here your command" name="command_'+count+'" id="command_input"></td>'
        html +='        <td style="width: 150px;">'
        html +='            <div class="btn-group" role="group"></div><select style="height: 28px;width: 120px;border-radius: 5px;" name="command_'+count+'_wait" id="wait_input"><option value="0" selected="">False</option><option value="1">True</option></select></td>'
        html +='    </tr>'
        html +='    </tbody>'
        html +='</table>'
        html +='</div>'
        document.getElementById(id).innerHTML = html

        document.getElementById("num_of_commands").innerHTML = '<input type="hidden" name="numcmds" value="'+count+'">'
        count += 1;
    }
}

function remove_command(){
    if(count >= 2){
        count -= 1
        let id = "cmd_"+count;
        document.getElementById(id).innerHTML = ""
        document.getElementById("num_of_commands").innerHTML = '<input type="hidden" name="numcmds" value="'+count+'">'
    }
}



