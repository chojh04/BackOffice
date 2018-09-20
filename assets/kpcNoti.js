var kpcNotiUtil = new function (){
	
	var table = {};
    
    this.readApprovalNotiList = function () {
    	setDataTable();
    }
    
    this.reload = function () {
    	table.fnFilter();
    }
       
    var setDataTable = function () {
    	
    	table = $('#approvalNotiTable')
            .on('click','.historyDetail', function () {
 	
            })  
            .dataTable(
                {
                    "processing": true,
                    "serverSide": true,
                    "destroy" : true,
                    "ajax": {
                        "url": "/api/approvals/answer/noti-list",
                        "async" : "true",
                        "error" : function (e){kpcUtil.sessionExpire(e);}
                    },
                    "ordering": false,
                    "drawCallback": function (settings) {
                    	
                    	if(settings.aiDisplay.length > 0) {
                    		$("#bellBtnIcon").append("<span class='badge bg-red'>"+settings.aiDisplay.length+"</span>")
                    	}
                    	else {
                    		$("#bellBtnIcon").empty();
                    	}
                    	
                        for (var i = 0, iLen = settings.aiDisplay.length; i < iLen; i++) {
                            settings.json.data[i].rownum = i + 1 + settings._iDisplayStart;
                        }
                        for (var i = 0, iLen = settings.aiDisplay.length; i < iLen; i++) {
                            $('td:eq(0)', settings.aoData[settings.aiDisplay[i]].nTr).html(i + 1 + Number(settings._iDisplayStart));
                            var detailBtn = '<a class="btn btn-sm green btn-outline" '
                            	+ 'href="/approval/answer/detail?apprSeq='+settings.json.data[i].seq
                           		+ '&apprWorkType='+settings.json.data[i].workType
                           		+ '&apprStatus='+settings.json.data[i].status
                           		+ '&entryPoint=noti'
                           		+ '" role="button">상세보기 </a>'
                            $('td:eq(8)', settings.aoData[settings.aiDisplay[i]].nTr).html(detailBtn)
                        }
                        
                    },
                    columns: [
                              {data: "rownum", defaultContent: "", width : 70, className: "column-align-center"},      // 번호
                              {	data: "workType", width : 150, defaultContent: "", className: "column-align-center",
                              	// 승인유형
                               	render : function (data, type , full , meta){
                                	return full.workTypeName; 
                               		}
                              },  
                              {	data: "refTitle", width : 250,  defaultContent: "", className: "column-align-center" }, //키워드
                              {
                              	data: "reqType", width : 150, defaultContent: "", className: "column-align-center",
                             		// 처리구분
                               	render : function (data, type , full , meta){
                               		return full.reqTypeName;
                               		}
                              },
                              {	
                              	data: "status", width : 90, defaultContent: "", className: "column-align-center",
                              	// 진행상태
                              	render : function (data, type , full , meta){
                                	return full.statusName; 
	                                }
                              },
                              {
                              	// 신청일
                              	data : "reqDate" , defaultContent: "", width : 90, className: "column-align-center" ,
	                                render : function (data, type , full , meta){
	                                	return kpcUtil.setDateFormat(full.reqDate , "YYYY-MM-DD");
	                                }
                              },         
                              {
                              	// 처리일
                              	data : "apprDate" ,
	                                defaultContent: "",
	                                width : 90,
	                                className: "column-align-center" ,
	                                render : function (data, type , full , meta){
	                           			if (full.apprDate !== "") {
	  	                                	return kpcUtil.setDateFormat(full.apprDate , "YYYY-MM-DD");
	                           			}
	                           			else {
	                           				return "-";
	                           			}
	                                }
                              },   
                              {data: "reqEmpName", defaultContent: "", width : 90, className: "column-align-center"}, // 승인자
                              {data: "detail", defaultContent: "", width :90, className: "column-align-center"},      // 상세보기 버튼
                    ],
                    buttons: [],
                    "lengthMenu": [[5, 10, 20, 30, 50], [5, 10, 20, 30, 50]],
                    "pageLength": 5,
                    "dom": "<'row' <'col-md-8 col-sm-12'l><'col-md-4 col-sm-12'B>><'table-scrollable'tr><'row'<'col-md-6 col-sm-6'i><'col-md-6 col-sm-6'p>>",
                    responsive: true,
                    "language": {
                        "aria": {
                            "sortAscending": ": activate to sort column ascending",
                            "sortDescending": ": activate to sort column descending"
                        },
                        "info":"Total Record: _TOTAL_ Page : _PAGE_ / _PAGES_ ",
                        "emptyTable": "조회된 자료가 없습니다.",
                        "infoEmpty": "조회된 자료가 없습니다.",
                        "lengthMenu": "_MENU_",
                        "zeroRecords": "조회된 자료가 없습니다."
                    },
                }
            );
    }
}

$(document).ready(function (){
	
	kpcNotiUtil.readApprovalNotiList();
	
	$(".bellBtn").click(function (){
		$("#approvalNotificationModal").modal("show");
	});
});