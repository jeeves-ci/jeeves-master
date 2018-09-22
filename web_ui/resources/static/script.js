$( document ).ready(function() {
    var activeSocket = new socketDetails();
    var url = window.location.href;
    var arr_url = url.split("/");
    var webUiPublicIp = arr_url[2];
    var arrIp = webUiPublicIp.split(":");
    var restfulPublicIp = arrIp[0] + ":8080";

    var url = `http://${restfulPublicIp}/api/v1.0/workflows`;

    var $pagination = $('#pagination'),
    totalRecords = 10,
    recPerPage = 2,
    page = 1,
    totalPages = Math.ceil(totalRecords / recPerPage);

    function apply_pagination() {
          $pagination.twbsPagination({
                totalPages: totalPages,
                visiblePages: 3,
                first: '',
                last: '',
                onPageClick: function (event, page) {
                      $.ajax({
                          url: url + '?page=' + page + '&size=' + recPerPage,
                          success: onWorkflowsListReceive
                      });
                }
          });
    }
    apply_pagination();
//    $.ajax({
//        url,
//        success: onWorkflowsListReceive
//    });

    function socketDetails(socket, taskID) {
        this.socket = socket;
        this.taskID = taskID;
        this.isActive = function (taskID) {
            return this.socket && this.taskID == taskID;
        };
        this.close = function () {
            if (this.socket) {
                this.socket.close();
                this.socket = undefined;
                this.taskID = undefined;
            }
        };
    }

    function onWorkflowsListReceive(data) {
        var workflowCont = $('.workflow_list');
        workflowCont.empty();
        totalRecords = data.total;
        $.each(data.workflows, function (index, workflow) {
            var linkObj = $('<a>',{
                    text: workflow.workflow_id,
                    title: 'Workflow Id: ' + workflow.workflow_id,
                    wfId: workflow.workflow_id,
                    href: '#',
                    click: onWorkflowClick.bind(workflow.workflow_id)
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
        listCont.empty();
        $.each(data.tasks, function (index, taskObj) {
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

        // Socket will be closed on window exit or on
        // switching to different task.
        if (activeSocket.isActive(taskId)) {
            return;
        } else {
            activeSocket.close();
        }
        activeSocket = openSocket(taskId);
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
        return new socketDetails(ws, taskId);
    }
});
