$( document ).ready(function() {
    console.log("ready!");
    var url = window.location.href;
    var arr_url = url.split("/");
    var webUiPublicIp = arr_url[2];
    var arrIp = webUiPublicIp.split(":");
    var restfulPublicIp = arrIp[0] + ":8080";

    var url = `http://${restfulPublicIp}/api/v1.0/workflows`;
    $.ajax({
        url,
        success: onWorkflowsListRecieve
    });

    function onWorkflowsListRecieve(data) {
        var workflowCont = $('.workflow_list');
        $.each(data, function (index, workflow) {
            var linkObj = $('<a>',{
                    text: 'Workflow Id: ' + workflow.workflow_id,
                    title: 'Workflow Id: ' + workflow.workflow_id,
                    wfId: workflow.workflow_id,
                    href: '#',
                    click: onWorkflowClick.bind(workflow)
                }),
                liObj = $('<li>').append(linkObj);
            workflowCont.append(liObj);
        })
    }

    function onWorkflowClick(event){
        var target = event.target,
            workflowId = $(target).attr('wfId'),
            url = `http://${restfulPublicIp}/api/v1.0/tasks?workflow_id=${workflowId}`

        $.ajax({
            url,
            success: onTaskDataListReceive
        });
    }

    function onTaskDataListReceive(data) {
        var listCont = $('.taskTabList_cont');
        listCont.html("");
        $.each(data, function (index, taskObj) {
            var linkObj = $('<a>',{
                    text: taskObj.task_name,
                    href: '#',
                    taskId: taskObj.task_id,
                    workflowId: taskObj.workflow_id,
                    click: onTaskClick.bind(taskObj.taskId)
                }),
                liObj = $('<li>').append(linkObj);
                listCont.append(liObj);
        })
    }

    function onTaskClick(event) {
        var target = event.target,
            taskId = $(target).attr('taskId');

        openSocket(taskId);
    }

    function openSocket(taskId){
        var ws = new WebSocket(`ws://${webUiPublicIp}/tail/${taskId}`);
        var $message = $('#message');
        var $content = $('#content');
        $content.html('');
        ws.onopen = function(){
            $message.attr("class", 'label label-success');
            $message.text('open');
        };
        ws.onmessage = function(ev){
            $message.attr("class", 'label label-info');
            $message.hide();
            $message.fadeIn("fast");
            $message.text('received message');
            console.log(ev.data);
            $content.append(ev.data);
        };
        ws.onclose = function(ev){
            $message.attr("class", 'label label-important');
            $message.text('closed');
        };
        ws.onerror = function(ev){
            $message.attr("class", 'label label-warning');
            $message.text('error occurred');
        };
    }
});
