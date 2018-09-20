var kpcPopupUtil = new function (){
	var table;
	this.openUserSearchPop = function (param){
    	var bodyHtml = ''
    	    +'<div class="col-md-12 col-sm-12 col-xs-12">'
    	    +'    <div class="x_panel">'
    	    +'        <div class="x_content form">'
    	    +'            <form action="javascript:nothing()" id="employeeMng" class="form-bordered ">'
    	    +'                <div class="col-md-12 col-sm-12 col-xs-12">'
    	    +'                    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
    	    +'                        <label class="control-label col-md-3 col-sm-3 col-xs-12" for="first-name">- 검색 조건 </label>'
    	    +'                    </div>'
    	    +'                </div>'
    	    +'                <div class="col-md-12 col-sm-12 col-xs-12">'
    	    +'                    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
    	    +'                        <label class="control-label col-lg-3 col-md-12 col-sm-3 col-xs-12" for="first-name">사원명</label>'
    	    +'                        <div class="col-lg-9 col-md-12 col-sm-9 col-xs-12 form-inline">'
    		+'							<input type="text" id="name" name="name" class="form-control col-md-7 col-xs-12">'
    	    +'                        </div>'
    	    +'                    </div>'
    	    +'                    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-right form-border-left-xs">'
    	    +'                        <label class="control-label col-lg-3 col-md-12 col-sm-3 col-xs-12" for="first-name">부서별</label>'
    	    +'                        <div class="col-lg-9 col-md-12 col-sm-9 col-xs-12 ">'
    	    +'                            <select class="select2_single select2-selection--single form-control" id="divisionId" name="divisionId" >'
    	    +'                                <option value="">전체</option>'
    	    +'                            </select>'
    	    +'                        </div>'
    	    +'                    </div>'
    	    +'                    <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12 form-group form-border-left form-border-right ">'
    	    +'                        <label class="control-label col-lg-3 col-md-12 col-sm-12 col-xs-12" for="first-name">팀별</label>'
    	    +'                        <div class="col-lg-9 col-md-12 col-sm-12 col-xs-12 form-inline">'
    	    +'                            <select class="select2_single select2-selection--single form-control" id="teamId" name="teamId" >'
    	    +'                                <option value="">전체</option>'
    	    +'                            </select>'
    	    +'                        </div>'
    	    +'                    </div>'
    	    +'                </div>'
    	    +'            </form>'
    	    +'            <br />'
    	    +'            <table id="employeeMngTable" class="table table-striped table-bordered">'
    	    +'                <thead>'
    	    +'                    <tr>'
    	    +'                        <th>순번</th>'
    	    +'                        <th>사번</th>'
    	    +'                        <th>부서</th>'
    	    +'                        <th>팀</th>'
    	    +'                        <th>이름</th>'
    	    +'                        <th>직위</th>'
    	    +'                    </tr>'
    	    +'                </thead>'
    	    +'                <tbody>'
    	    +'                </tbody>'
    	    +'            </table>'
    	    +'        </div>'
    	    +'    </div>'
    	    +'</div>'
    		;
    	kpcUtil.openCommonPopup({
    		modalTitle : "사용자 조회",
    		bodyHtml : bodyHtml,
    		modalSize : "modal-full",
    		buttonEvent : [
    		               // 모달 이벤트
    		               {
    		            	   target : ".modal",
    		            	   eventType : "shown.bs.modal",
    		            	   callBack : function (){
    		                       table = $('#employeeMngTable')
    		                       .on('click', '.empSelect', function () {
    		                    	   param.callBackFunction($(this).attr("empId"));
    		                    	   $(".modal").modal('hide');
    		                       })     
    		                       .dataTable(
    		                           {
    		                               "processing": true,
    		                               "serverSide": true,
    		                               "ajax": {
    		                                   "url": "/api/systemMng/employees",
    		                                   "async" : "true",
    		                                   "data": function (parameter) {
    		                                       parameter.formData = $("#employeeMng").serializeObject();
    		                                   },
    		                                   "error" : function (e){kpcUtil.sessionExpire(e);}
    		                               },
    		                               "ordering": false,
    		                               "drawCallback": function (settings) {
    		                                   for (var i = 0, iLen = settings.aiDisplay.length; i < iLen; i++) {
    		                                       $('td:eq(0)', settings.aoData[settings.aiDisplay[i]].nTr).html(i + 1 + settings._iDisplayStart);
    		                                       settings.json.data[i].rownum = i + 1 + settings._iDisplayStart;
    		                                   }
    		                               },
    		                               columns: [
    		                                   {data: "rownum", defaultContent: "", width : 80, className: "column-align-right"}, // 순번
    		                                   {data: "employeeId", defaultContent: "",  className: "column-align-center"},                    // 사번
    		                                   {data: "divisionName", defaultContent: "",className: "column-align-center"},                   // 부서
    		                                   {data: "teamName", defaultContent: "",className: "column-align-center"},                // 팀
    		                                   {
    		                                   	data : "name" ,
    		   	                                defaultContent: "", 
    		   	                                className: "column-align-center",
    		   	                                render : function (data, type , full , meta){
    		   	                                	return '<a class="blue empSelect" href="javascript:;" empId="' + full.employeeId + '" >' + full.name + '</a>';
    		   	                                }
    		                                   },  // 구분    		                                   
    		                                   {data: "positionName", defaultContent: "", className: "column-align-center"},   // 직위
    		                               ],
    		                               buttons: [
    		                                   {
    		                                       text: '조회',
    		                                       className: 'btn green btn-outline ',
    		                                       action: function (e, dt, node, config) {
    		                                    	   table.fnFilter();
    		                                       }
    		                                   }
    		                               ],
    		                               "lengthMenu": [[10, 20, 30, 50, 200], [10, 20, 30, 50, 200]],
    		                               "pageLength": 10,
    		                               "dom": "<'row' <'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'B>><'table-scrollable'tr><'row'<'col-md-6 col-sm-6'i><'col-md-6 col-sm-6'p>>",
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
    		              ,{
   		            	   target : ".closeBtn",
		            	   eventType : "click",
		            	   callBack : function (){
	                    	   param.callBackFunction();
		            	   }
    		              }
    		              ]
    	});    	
    }
    
    /**
     * 사용자 별 테이블 column 관리
     * openTableColumnMng function 에서 관리한 column 정보를 기반으로 
     * 화면내의 show/hide column을 설정한다.
     */
    this.setUserTableColumnData = function (param){
		 $.ajax({
             type: 'POST',
             dataType : "json",
             contentType  : "application/json",
			  url : "/api/systemMng/common/getTableColumnMng",
			  data : JSON.stringify({
				   "menuId"   : param.menuId
				  ,"tableId"  : param.tableId
			  }),
		  }).done(function (serachData){
			  kpcPopupUtil.setUserTableColumnMng(serachData.descText,param.tableId,param.targetTable);
		  }).fail(function  (xhr , status,  error){
			  kpcUtil.errorHandling(error);
		  });       	
    }
    
    this.openTableColumnMng = function (param){
    	var serachData = {};
    	var setTableColumn = function (){
    		var columnObj = {};
    		if(typeof serachData !== "undefined" && serachData.length > 0 ){
    			var dataSplit = serachData.split("^");
    			for(var idx in dataSplit){
    				var position = dataSplit[idx].indexOf(":");
    				if (dataSplit[idx].substring(0,position) != ""){
    					columnObj[dataSplit[idx].substring(0,position) + ""] = dataSplit[idx].substring(position+1);
    				}
    			}
    		}
		    var columnHtml = "";
		    $("#"+ param.tableId + " thead>tr>th").each(function (){
		  	    var title = $(this).text().trim();
		  	    if (title != ""){
		  	    	var checkedHtml = 'checked="checked"';
	  	    		for(var key in columnObj){
	  	    			if(key == title && (columnObj[key] == "false" )){
	  	    				checkedHtml = '"' 
	  	    			}
	  	    		}
	  	    		console.log(checkedHtml);
		  	  	    columnHtml += "<tr>"
		  	  	  	+ "<td>"
		  	  	  	+ title
		  	  	  	+ "</td>"
		  	  	  	+ "<td align='center'>"
		  	  	  	+ '<label class="mt-checkbox mt-checkbox-single mt-checkbox-outline">'
		  	  	  	+ '<input type="checkbox" class="checkboxes" name="chk" '
		  	  	    +  checkedHtml
		  	  	  	+ '>'
		  	  	  	+ '<span></span>'
		  	  	  	+ '</label>';
		  	  	    + "</td>"
		  	  	    + "</tr>";
		  	    }
		    });
		    $("#tableColumnMng table>tbody").html("");
		    $("#tableColumnMng table>tbody").append(columnHtml);    		
    	}
    	var bodyHtml = ''
    	    +'<div class="col-md-12 col-sm-12 col-xs-12">'
    	    +'    <div class="x_panel">'
    	    +'        <div class="x_content form">'
    	    +'            <form action="javascript:nothing()" id="tableColumnMng" class="form-bordered ">'
    	    +'                <div class="col-md-12 col-sm-12 col-xs-12">'
    	    +'                     <table class="table">'
    		+'                         <thead>'
    		+'                         	   <tr>'
    		+'                         	   	   <th>조회항목</th>'
    		+'                         	   	   <th>화면표시여부</th>'
    		+'                         	   </tr>'
    		+'                         </thead>'
    		+'                         <tbody></tbody>'
    		+'                     </table>'
    	    +'                </div>'
    	    +'            </form>'
    	    +'        </div>'
    	    +'    </div>'
    	    +'</div>'
    		;
    	var buttonHtml = '<button type="button" class="dt-button btn red btn-outline btnClear">초기화</button>'
    		           + '<button type="button" class="dt-button btn green btn-outline btnSave">확인</button>';
    	kpcUtil.openCommonPopup({
    		modalTitle : "데이터 설정",
    		popupType : "layout",
    		bodyHtml : bodyHtml,
    		button : buttonHtml,
    		modalSize : "modal-sm",
    		buttonEvent : [
    		               // 모달 이벤트
    		               {
    		            	   target : ".modal",
    		            	   eventType : "shown.bs.modal",
    		            	   callBack : function (){
    		            		   
 		            			 $.ajax({
		                              type: 'POST',
		                              dataType : "json",
		                              contentType  : "application/json",
		            				  url : "/api/systemMng/common/getTableColumnMng",
		            				  data : JSON.stringify({
		            					   "menuId"   : param.menuId
		            					  ,"tableId"  : param.tableId
		            				  }),
		            			  }).done(function (data){
		            				  serachData = data.descText;
		            				  setTableColumn();
		            			  }).fail(function  (xhr , status,  error){
		            				  kpcUtil.errorHandling(error);
		            			  });    		            		   
    		            		   
    		            	   }
    		               }
    		              ,{
    		            	  target : "button.btnClear",
    		            	  eventType : "click",
    		            	  callBack : function (){
    		            		  setTableColumn();
    		            	  }
    		              }
    		              ,{
    		            	  target : "button.btnSave",
    		            	  eventType : "click",
    		            	  callBack : function (){
    		            		  if(kpcUtil.confirm("저장 하시겠습니까?")){
    		            			  var displayData = "";
    		            			  $("#tableColumnMng table>tbody>tr").each(function (){
    		            				  displayData += $(this).find("td").text() + ":"+ $(this).find("td").eq(1).find("input[name=chk]").is(":checked") + "^";
    		            			  });
    		            			  $.ajax({
    		                              type: 'POST',
    		                              dataType : "json",
    		                              contentType  : "application/json",
    		            				  url : "/api/systemMng/common/tableColumnMng",
    		            				  data : JSON.stringify({
    		            					   "menuId"   : param.menuId
    		            					  ,"tableId"  : param.tableId
    		            					  ,"descText" : displayData
    		            				  }),
    		            			  }).done(function (data){
    		            				  kpcUtil.successHandling("",data,false);
    		            				  $(".modal").modal('hide');
    		            			  }).fail(function  (xhr , status,  error){
    		            				  kpcUtil.errorHandling(error);
    		            			  });
    		            			  // table show/hide 처리 
    		            			  kpcPopupUtil.setUserTableColumnMng(displayData,param.tableId,param.targetTable);
    		            		  }
    		            		  

    		            	  }
    		              }
    		              ]
    	});    	
    }
    
    this.setUserTableColumnMng = function (displayData,tableId,targetTable){
    	if(typeof displayData !== "undefined"){
    		// 저장 후 화면에 적용
    		var dataSplit = displayData.split("^");
    		for(var idx in dataSplit){
    			var position = dataSplit[idx].indexOf(":");
    			var title = dataSplit[idx].substring(0,position);
    			var flag = dataSplit[idx].substring(position+1);
				$("#"+ tableId + " thead>tr>th").each(function (){
						if($(this).text().trim() == title){
							if (flag == "false"){
								$(this).hide();
								$("#"+ tableId + " tr").find("td:eq('"+$(this)[0].cellIndex+"')").hide();
							}else {
								$(this).show();
								$("#"+ tableId + " tr").find("td:eq('"+$(this)[0].cellIndex+"')").show();
							}
						}
				});
    		}    	
    	}
    }
    this.openKconHistoryModal = function (param){
		var bodyHtml = ''
 	         + '<table id="historyTable" class="table table-striped table-bordered" style="width: 100%">'
           + '    <thead>'
           + '        <tr>'
           + '            <th>순번</th>'
           + '            <th>등록일시</th>'
           + '            <th>구분</th>'
           + '            <th>연장일</th>'
           + '            <th>사유</th>'
           + '            <th>등록자</th>'
           + '        </tr>'
           + '    </thead>'
           + '    <tbody>'
           + '    </tbody>'
		        + '</table>'
           ;
  		kpcUtil.openCommonPopup({
  			modalTitle : "등록이력조회",
  			bodyHtml : bodyHtml,
  			modalSize : "custom-md-modal-body",
  			buttonEvent : [
  			  // 모달 이벤트
  			  {
  			  	target : ".modal",
  			  	eventType : "shown.bs.modal",
  			  	callBack : function (){
  		            $('#historyTable')
  		            .dataTable({
  		                    "bProcessing": true,
  		                    "bServerSide": true,
  		                    "ajax": {
  		                        "url": "/api/systemMng/common/systemHistory",
  		                        "async" : "true",
  		                        "data": function (parameter) {
  		                            parameter.menuId = param.menuId;
  		                            parameter.desc1 = param.desc1;
  		                        },
  		                        "error" : function (e){kpcUtil.sessionExpire(e);}
  		                    },
  		                    "ordering": false,
                            "drawCallback": function (settings) {
                                for (var i = 0, iLen = settings.aiDisplay.length; i < iLen; i++) {
                                    $('td:eq(0)', settings.aoData[settings.aiDisplay[i]].nTr).html(i + 1 + settings._iDisplayStart);
                                    settings.json.data[i].rownum = i + 1 + settings._iDisplayStart;
                                }
                            },  		                    
  		                    columns: [
                                {data : "rownum" , defaultContent: "",width : 30, className: "column-align-right"}, // 순번 
                                {
                                  	data : "regDt" , 
  	                                defaultContent: "",
  	                                width : 90,
  	                                className: "column-align-center" ,  	                                
  	                                render : function (data, type , full , meta){
  	                                	return kpcUtil.setDateFormat(full.regDt, "YYYY-MM-DD HH:mm:ss");
  	                                }
                                }, // 등록일  		                        
  		                        {data: "typeName", defaultContent: "",  className: "column-align-center"}, // 구분
  		                        {data: "desc2", defaultContent: "",  className: "column-align-center"}, // 연장일
  		                        {data: "desc3", defaultContent: "",  className: "column-align-center"}, // 사유
  		                        {data: "regId", defaultContent: "",  className: "column-align-center"}, // 등록자
  		                    ],
  		                    "dom": "<'table-scrollable't>",
  		                    responsive: true,
  		                    "language": {
  		                        "aria": {
  		                            "sortAscending": ": activate to sort column ascending",
  		                            "sortDescending": ": activate to sort column descending"
  		                        },
  		                        "info":"Total Record: _TOTAL_ Page : _START_ / _PAGES_ ",
  		                        "emptyTable": "조회된 자료가 없습니다.",
  		                        "infoEmpty": "조회된 자료가 없습니다.",
  		                        "lengthMenu": "_MENU_",
  		                        "zeroRecords": "조회된 자료가 없습니다.",
  		                    },
		                    });
  			  	}
  			  }]
  		});    	
    }
    
    this.openApprListPop = function (param){
    	var menuId = param.menuId;
       	var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnSel">등록</button>';
       	kpcPopupUtil.openSecondPopup({
       		modalTitle : "승인자선택",
       		modalSize : "custom-sm-modal-body",
       		button : buttonHtml,
       		buttonEvent : [
               // 모달 이벤트
               {
            	   target : ".modal",
            	   eventType : "shown.bs.modal",
            	   callBack : function (){

            	       $.ajax({
            	           url: "/api/approval/getApprovers",
            	           data: "menuId=" + menuId,
            	           type: 'GET',
            	           dataType : "json",
            	       }).done(function(data){
            	    	   console.log(data)
            	    	   
            	    	   var bodyHtml = '<div class="col-md-12 col-sm-12 col-xs-12" id="apprDiv">'
        	    		   for(var idx in data){
        	    			   bodyHtml += '<div class="col-md-6 col-sm-6 col-xs-6">'
        	    				   +  '	<label class="mt-radio mt-radio-single mt-radio-outline">'
        	    				   +  '		<input type="radio" class="selCheckboxes" name="empList" value="1" empId="'+data[idx].empId + '"'
        	    				   +  ' 		menuId="'+data[idx].menuId+'">'
        	    				   +  '		<span></span>' + data[idx].name +' ('+data[idx].email+')'
        	    				   +  '	</label>'
        	    				   +  '</div>';
    	    			   }
            	    	   bodyHtml +='</div>';
            	    	   $(".dynamic-second-modal-body").html(bodyHtml);
            	    	   $("input[name=empList]")[0].focus();
        	    	   }).fail(function(e){
        	    		   kpcUtil.errorHandling(e);
    	    		   });
        	       }
               }
              ,{
	   				target : ".btnSel",
	   				eventType : "click",
	   				callBack : function (){
	   					param.callBack();
					}
	   			}]
       	});           	
    }     
    
    /**
     * jsonData : ,modalTitle : 모달 제목
     *            ,button  : 사용자 버튼 
     *            ,event   : body 호출 방식 
     *               - url : ajax 를 사용해서 body data를 가져온다
     *               - html : 호출 페이지에서 String 으로 전달
     *            ,url : modalType 이 "URL" 일 경우 사용
     *            ,params : modalType 이 "URL" 일 경우 사용 
     *                      queryString 형식의 parameter key1=val&key2=val2
     *            ,method : modalType 이 "URL" 일 경우 사용 
     *                    http method type
     *            ,bodyHtml : modalType 이 "URL"이 아닌경우 사용
     */
    this.openSecondPopup = function(jsonData){
    	try{
    		// 중복 실행 방지
    		$("input[type!=hidden]")[0].focus()
    	} catch(e){}    	
    	var modalSize = jsonData.hasOwnProperty('modalSize') ? jsonData.modalSize: "modal-md";
		var html = ''
			 + '<div class="modal fade" id="commonPopupModal2"  role="dialog" aria-labelledby="commonPopupModalLabel2">'
			 + '    <div class="modal-dialog '+modalSize+'" role="document">                                                  '
			 + '        <div class="modal-content">                                                                      '
			 + '            <div class="modal-header">                                                                   '
			 + '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
			 + '                        aria-hidden="true">&times;</span></button>                                       '
			 + '                <h4 class="modal-title" style="text-align:center;" id="commonPopupModalLabel2">'+jsonData.modalTitle+'</h4>          '
			 + '            </div>                                                                                       '
			 + '            <div class="dynamic-second-modal-body modal-body form ">                     '
			 + '            </div>                                                                                       '
			 + '            <div class="modal-footer">                                                                   ';
		if(jsonData.hasOwnProperty('button')){
			html+= jsonData.button;
		}
		html+='                <button type="button" class="dt-button btn red btn-outline closeBtn" data-dismiss="modal">닫기</button>'
		 	 + '            </div>                                                                                       '
			 + '        </div>                                                                                           '
			 + '    </div>                                                                                               '
			 + '</div>';
		$("#commonPopupModal2").remove();
		$(".right_col").append(html);
    	if(jsonData.hasOwnProperty('modalType') && jsonData.modalType === "URL"){
    		kpcUtil.getAjaxContent(jsonData.URL,jsonData.params, jsonData.method, ".dynamic-second-modal-body");
    	}else{
    		$(".dynamic-second-modal-body").html(jsonData.bodyHtml);
    	}
    	if(jsonData.hasOwnProperty('buttonEvent')){
    		for(var idx in jsonData.buttonEvent){
    			$(jsonData.buttonEvent[idx].target).unbind(jsonData.buttonEvent[idx].eventType);
    			$(jsonData.buttonEvent[idx].target).on(jsonData.buttonEvent[idx].eventType ,jsonData.buttonEvent[idx].callBack);
    		}
    	}
    	$("#commonPopupModal2").modal({backdrop: 'static'}).on("hidden.bs.modal",function (){
    		$(this).remove();
    	});;
    }
    
    /**
     * jsonData : ,modalTitle : 모달 제목
     *            ,button  : 사용자 버튼 
     *            ,event   : body 호출 방식 
     *               - url : ajax 를 사용해서 body data를 가져온다
     *               - html : 호출 페이지에서 String 으로 전달
     *            ,url : modalType 이 "URL" 일 경우 사용
     *            ,params : modalType 이 "URL" 일 경우 사용 
     *                      queryString 형식의 parameter key1=val&key2=val2
     *            ,method : modalType 이 "URL" 일 경우 사용 
     *                    http method type
     *            ,bodyHtml : modalType 이 "URL"이 아닌경우 사용
     */
    this.openThridPopup = function(jsonData){
    	try{
    		// 중복 실행 방지
    		$("input[type!=hidden]")[0].focus()
    	} catch(e){}    	
    	var modalSize = jsonData.hasOwnProperty('modalSize') ? jsonData.modalSize: "modal-md";
    	var html = ''
    		+ '<div class="modal fade" id="commonPopupModal3"  role="dialog" aria-labelledby="commonPopupModalLabel2">'
    		+ '    <div class="modal-dialog '+modalSize+'" role="document">                                                  '
    		+ '        <div class="modal-content">                                                                      '
    		+ '            <div class="modal-header">                                                                   '
    		+ '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span        '
    		+ '                        aria-hidden="true">&times;</span></button>                                       '
    		+ '                <h4 class="modal-title" style="text-align:center;" id="commonPopupModalLabel2">'+jsonData.modalTitle+'</h4>          '
    		+ '            </div>                                                                                       '
    		+ '            <div class="dynamic-third-modal-body modal-body form ">                     '
    		+ '            </div>                                                                                       '
    		+ '            <div class="modal-footer">                                                                   ';
    	if(jsonData.hasOwnProperty('button')){
    		html+= jsonData.button;
    	}
    	html+='                <button type="button" class="dt-button btn red btn-outline closeBtn" data-dismiss="modal">닫기</button>'
    		+ '            </div>                                                                                       '
    		+ '        </div>                                                                                           '
    		+ '    </div>                                                                                               '
    		+ '</div>';
    	$("#commonPopupModal3").remove();
    	$(".right_col").append(html);
    	if(jsonData.hasOwnProperty('modalType') && jsonData.modalType === "URL"){
    		kpcUtil.getAjaxContent(jsonData.URL,jsonData.params, jsonData.method, ".dynamic-second-modal-body");
    	}else{
    		$(".dynamic-third-modal-body").html(jsonData.bodyHtml);
    	}
    	if(jsonData.hasOwnProperty('buttonEvent')){
    		for(var idx in jsonData.buttonEvent){
    			$(jsonData.buttonEvent[idx].target).unbind(jsonData.buttonEvent[idx].eventType);
    			$(jsonData.buttonEvent[idx].target).on(jsonData.buttonEvent[idx].eventType ,jsonData.buttonEvent[idx].callBack);
    		}
    	}
    	$("#commonPopupModal3").modal({backdrop: 'static'}).on("hidden.bs.modal",function (){
    		$(this).remove();
    	});
    }
    
    this.openPromptPop = function (param){
    	var confirmMsg = param.confirmMsg;
    	var confirmTitle = param.confirmTitle;
   		var bodyHtml = '<div class="row" style="margin-top:10px;">'
	        + '<div class="col-md-12 col-sm-12 col-xs-12">'
	        + '    <div class="col-md-12 col-sm-12 col-xs-12 form-group ">'
	        + '        <label class="control-label col-md-12 col-sm-12 col-xs-12"><b>'+confirmMsg+'</b></label>'
	        + '     </div>'
	        + '</div>'
            + '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 form-group">'
            + '    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'
	        + '        <input type="text" id="desc2" name="desc2" class="form-control col-md-7 col-xs-12">'
            + '    </div>'
            + '</div>'
            + '</div>'
	         ;
   		var buttonHtml = '<button type="button" class="dt-button btn green btn-outline btnPromptConfirm">확인</button>';
   		kpcPopupUtil.openThridPopup({
   			modalTitle : confirmTitle,
   			bodyHtml : bodyHtml,
   			button : buttonHtml,
   			modalSize : "custom-sm-modal-body",
   			buttonEvent : [{
   				target : ".btnPromptConfirm",
   				eventType : "click",
   				callBack : function (){
   					if($("#desc2").val().trim().length < 5){
   						kpcUtil.customAlert("사유를 5자이상 적어주세요.");
   						return false;
   					}
   					param.promptCallback($(desc2).val());
				}
   			}]
   		});    	
    }    
}