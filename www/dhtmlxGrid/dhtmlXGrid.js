/*_TOPICS_
@0:initialization
@1:selection control
@2:rows control
@3:colums control
@4:cells controll
@5:data manipulation
@6:appearence control
@7:overal control
@8:tools
@9:treegrid
@10: event handlers
@11: paginal output
*/

var globalActiveDHTMLGridObject;
String.prototype._dhx_trim = function(){
                     return this.replace(/&nbsp;/g," ").replace(/(^[ \t]*)|([ \t]*$)/g,"");
                  }


function dhtmlxArray(ar){ return dhtmlXHeir((ar||new Array()),new _dhtmlxArray()); };
function _dhtmlxArray(){ return this; };
_dhtmlxArray.prototype._dhx_find = function(pattern){
   for(var i=0;i<this.length;i++){
      if(pattern==this[i])
            return i;
   }
   return -1;
}
_dhtmlxArray.prototype._dhx_delAt = function(ind){
   if(Number(ind)<0 || this.length==0)
      return false;
   for(var i=ind;i<this.length;i++){
      this[i]=this[i+1];
   }
   this.length--;
}
_dhtmlxArray.prototype._dhx_insertAt = function(ind,value){
   this[this.length] = null;
   for(var i=this.length-1;i>=ind;i--){
      this[i] = this[i-1]
   }
   this[ind] = value
}
_dhtmlxArray.prototype._dhx_removeAt = function(ind){
   for(var i=ind;i<this.length;i++){
      this[i] = this[i+1]
   }
   this.length--;
}
_dhtmlxArray.prototype._dhx_swapItems = function(ind1,ind2){
   var tmp = this[ind1];
   this[ind1] = this[ind2]
   this[ind2] = tmp;
}

/**
*   @desc: dhtmlxGrid constructor
*   @param: id - (optional) id of div element to base grid on
*   @returns: dhtmlxGrid object
*   @type: public
*/
function dhtmlXGridObject(id){
   if (_isIE) try { document.execCommand("BackgroundImageCache", false, true); } catch (e){}
   if(id){
      if(typeof(id)=='object'){
         this.entBox = id
         this.entBox.id = "cgrid2_"+(new Date()).getTime();
      }else
         this.entBox = document.getElementById(id);
   }else{
      this.entBox = document.createElement("DIV");
      this.entBox.id = "cgrid2_"+(new Date()).getTime();
   }

    this.dhx_Event();

    this._tttag=this._tttag||"rows";
    this._cttag=this._cttag||"cell";
    this._rttag=this._rttag||"row";

   var self = this;

    this._wcorr=0;
   this.nm = this.entBox.nm || "grid";
   this.cell = null;
   this.row = null;
   this.editor=null;
    this._f2kE=true; this._dclE=true;
   this.combos=new Array(0);
    this.defVal=new Array(0);
   this.rowsAr = new Array(0);//array of rows by idd
   this.rowsCol = new dhtmlxArray(0);//array of rows by index
    //this.hiddenRowsAr = new Array(0);//nb added for paging
   this._maskArr=new Array(0);
   this.selectedRows = new dhtmlxArray(0);//selected rows array
   this.rowsBuffer = new Array(new dhtmlxArray(0),new dhtmlxArray(0));//buffer of rows loaded, but not rendered (array of ids, array of cell values arrays)
   this.loadedKidsHash = null;//not null if there is tree cell in grid
   this.UserData = new Array(0)//array of rows (and for grid - "gridglobaluserdata") user data elements

/*MAIN OBJECTS*/

   this.styleSheet = document.styleSheets;
      this.entBox.className += " gridbox";
     
       this.entBox.style.width = this.entBox.getAttribute("width") ||   (window.getComputedStyle?(this.entBox.style.width||window.getComputedStyle(this.entBox,null)["width"]):(this.entBox.currentStyle?this.entBox.currentStyle["width"]:0)) || "100%";
       this.entBox.style.height = this.entBox.getAttribute("height") || (window.getComputedStyle?(this.entBox.style.height||window.getComputedStyle(this.entBox,null)["height"]):(this.entBox.currentStyle?this.entBox.currentStyle["height"]:0)) || "100%";
      //cursor and text selection
      this.entBox.style.cursor = 'default';
        this.entBox.onselectstart = function(){return false};//avoid text select
   this.obj = document.createElement("TABLE");
      this.obj.cellSpacing = 0;
      this.obj.cellPadding = 0;
      this.obj.style.width = "100%";//nb:
      this.obj.style.tableLayout = "fixed";
      this.obj.className = "c_obj".substr(2);

        this.obj._rows=function(i){ return this.rows[i+1]; }
        this.obj._rowslength=function(){ return this.rows.length-1; }

   this.hdr = document.createElement("TABLE");
        this.hdr.style.border="1px solid gray";  //FF 1.0 fix
      this.hdr.cellSpacing = 0;
      this.hdr.cellPadding = 0;
      if ((!_isOpera)||(_OperaRv>=8.5))
             this.hdr.style.tableLayout = "fixed";
      this.hdr.className = "c_hdr".substr(2);
      this.hdr.width = "100%";

   this.xHdr = document.createElement("TABLE");
   	  this.xHdr.className = "xhdr";
      this.xHdr.cellPadding = 0;
      this.xHdr.cellSpacing = 0;
      this.xHdr.style.width='100%'
      var r = this.xHdr.insertRow(0)
      var c = r.insertCell(0);
         r.insertCell(1).innerHTML = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
         r.childNodes[1].style.width='100%';
         c.appendChild(this.hdr)
   this.objBuf = document.createElement("DIV");
      this.objBuf.appendChild(this.obj);
   this.entCnt = document.createElement("TABLE");
      this.entCnt.insertRow(0).insertCell(0)
      this.entCnt.insertRow(1).insertCell(0);



      this.entCnt.cellPadding = 0;
      this.entCnt.cellSpacing = 0;
      this.entCnt.width = "100%";
      this.entCnt.height = "100%";

          this.entCnt.style.tableLayout = "fixed";

   this.objBox = document.createElement("DIV");
      this.objBox.style.width = "100%";
      this.objBox.style.height = this.entBox.style.height;
      this.objBox.style.overflow = "auto";
      this.objBox.style.position = "relative";
      this.objBox.appendChild(this.objBuf);
      this.objBox.className = "objbox";


   this.hdrBox = document.createElement("DIV");
      this.hdrBox.style.width = "100%"
        if (((_isOpera)&&(_OperaRv<9)) )
            this.hdrSizeA=25; else this.hdrSizeA=200;

           this.hdrBox.style.height=this.hdrSizeA+"px";
       if (_isIE)
            this.hdrBox.style.overflowX="hidden";
      else
          this.hdrBox.style.overflow = "hidden";

      this.hdrBox.style.position = "relative";
      this.hdrBox.appendChild(this.xHdr);



   this.preloadImagesAr = new Array(0)

   this.sortImg = document.createElement("IMG")
   this.sortImg.style.display = "none";
   this.hdrBox.insertBefore(this.sortImg,this.xHdr)
    this.entCnt.rows[0].cells[0].vAlign="top";
   this.entCnt.rows[0].cells[0].appendChild(this.hdrBox);
   this.entCnt.rows[1].cells[0].appendChild(this.objBox);


   this.entBox.appendChild(this.entCnt);
   //add links to current object
   this.entBox.grid = this;
   this.objBox.grid = this;
   this.hdrBox.grid = this;
   this.obj.grid = this;
   this.hdr.grid = this;
/*PROPERTIES*/
   this.cellWidthPX = new Array(0);//current width in pixels
   this.cellWidthPC = new Array(0);//width in % if cellWidthType set in pc
   this.cellWidthType = this.entBox.cellwidthtype || "px";//px or %

   this.delim = this.entBox.delimiter || ",";
   this._csvDelim = ",";

   this.hdrLabels = (this.entBox.hdrlabels || "").split(",");
   this.columnIds = (this.entBox.columnids || "").split(",");
   this.columnColor = (this.entBox.columncolor || "").split(",");
   this.cellType =  dhtmlxArray((this.entBox.cellstype || "").split(","));
   this.cellAlign =  (this.entBox.cellsalign || "").split(",");
   this.initCellWidth = (this.entBox.cellswidth || "").split(",");
   this.fldSort = (this.entBox.fieldstosort || "").split(",")
   this.imgURL = this.entBox.imagesurl || "gridCfx/";
   this.isActive = false;//fl to indicate if grid is in work now
   this.isEditable = true;
   this.raNoState = this.entBox.ranostate || null;
   this.chNoState = this.entBox.chnostate || null;
   this.selBasedOn = (this.entBox.selbasedon || "cell").toLowerCase()
   this.selMultiRows = this.entBox.selmultirows || false;
   this.multiLine = this.entBox.multiline || false;
   this.noHeader = this.entBox.noheader || false;
   this.xmlFileUrl = this.entBox.xmlfileurl || "";
   this.recordsNoMore = this.entBox.infinitloading || true;;//if true, then it will not attempt to fill the buffer from server
   this.useImagesInHeader = false;//use images in header or not
   this.pagingOn = false;//paging on/off
   this.rowsBufferOutSize = 0;//number of rows rendered at a moment
/*EVENTS*/
   dhtmlxEvent(window,"unload",function(){try{ self.destructor(); } catch(e){}});

/*XML LOADER(S)*/
   /**
   *   @desc: loads xml content from specified url into grid
   *   @param: url - XML file url
   *   @param: afterCall - function which will be called after xml loading
   *   @type: public
   *   @topic: 0,5
   */
   this.loadXML = function(url,afterCall){ 
        if (this._dload) { this._dload=url; this._askRealRows(null,afterCall); return true; };
        if (this._xmlaR) this.setXMLAutoLoading(url);


      if(url.indexOf("?")!=-1)
         var s = "&";
      else
         var s = "?";
      var obj = this;
	  this.callEvent("onXLS",[this]);

      if (afterCall) this.xmlLoader.waitCall=afterCall;
      this.xmlLoader.loadXML(url+""+s+"rowsLoaded="+this.getRowsNum()+"&lastid="+this.getRowId(this.getRowsNum()-1));
     
       //nb:
      //if (this.onXLS) setTimeout(function(){obj.onXLS(obj)},0);
      //setTimeout(function(){obj.xmlLoader.loadXML(url+""+s+"rowsLoaded="+obj.getRowsNum()+"&lastid="+obj.getRowId(obj.getRowsNum()-1)+"&sn="+Date.parse(new Date()));},1)
   }

   /**
   *   @desc: set one of predefined css styles (xp, mt, gray, light, clear, modern)
   *   @param: name - style name
   *   @type: public
   *   @topic: 0,6
   */
   this.setSkin = function(name){
      this.entBox.className = "gridbox gridbox_"+name;
      this.enableAlterCss("ev_"+name,"odd_"+name,this.isTreeGrid())
      this._fixAlterCss()      
      this._sizeFix=this._borderFix=0;
      switch(name){
      	 case "clear":
      	 	this._topMb=document.createElement("DIV");
      	 	this._topMb.className="topMumba";
      	 	this._topMb.innerHTML="<img style='left:0px'   src='"+this.imgURL+"skinC_top_left.gif'><img style='right:0px' src='"+this.imgURL+"skinC_top_right.gif'>";
      	 	this.entBox.appendChild(this._topMb);
      	 	this._botMb=document.createElement("DIV");
      	 	this._botMb.className="bottomMumba";
			this._botMb.innerHTML="<img style='left:0px'   src='"+this.imgURL+"skinD_bottom_left.gif'><img style='right:0px' src='"+this.imgURL+"skinD_bottom_right.gif'>";
      	 	this.entBox.appendChild(this._botMb);      	 	
      	 	this.entBox.style.position="relative";
      	 	this._gcCorr=20;
      	 	break;
      	 case "modern":
      	 case "light": 
  	 		this.forceDivInHeader=true;
  	 		this._sizeFix=1;
      	 	break;
         case "xp":    	 		this.forceDivInHeader=true; this._srdh=22; this._sizeFix=1; break;
		 case "mt":
		 	this._srdh=22;
		 	this._sizeFix=1;
		 	this._borderFix=(_isIE?1:0);break;
		 break;
		 case "gray": if ((_isIE)&&(document.compatMode != "BackCompat")) this._srdh=22;
		 	this._sizeFix=1;
		 	this._borderFix=(_isIE?1:0);break;
      }
      
      if (_isIE && this.hdr){
      	var d=this.hdr.parentNode;
      	d.removeChild(this.hdr);
      	d.appendChild(this.hdr);
      	}
      this.setSizes();
      	
   }

//#__pro_feature:21092006{
//#loadfrom_string:21092006{
   /**
   *   @desc: loads xml content from specified string
   *   @param: str - XML string
   *   @param: afterCall - function which will be called after xml loading
   *   @type: public
   *   @topic: 0,5
   *   @edition: Professional
   */
   this.loadXMLString = function(str,afterCall){
        if (this._dload) { this._dloadStr=str; this._askRealRows(null,afterCall); return true; };
		this.callEvent("onXLS",[this]);

      if (afterCall) this.xmlLoader.waitCall=afterCall;
      this.xmlLoader.loadXMLString(str);
   }
//#}
//#}
   /**
   *   @desc: puts xml to parser
   *   @type: private
   *   @topic: 0,5
   */
   this.doLoadDetails = function(obj){
      var root = self.xmlLoader.getXMLTopNode(self._tttag)
        if (root.tagName!="DIV")
	  if (self._refresh_mode){
		self._refreshFromXML(self.xmlLoader);
	  	self._refresh_mode=null;
	  }else
      if(!self.xmlLoader.xmlDoc.nodeName){
         self.parseXML(self.xmlLoader.xmlDoc.responseXML)
      }else{
         self.parseXML(self.xmlLoader.xmlDoc)
        }
      //nb:paging
      if(self.pagingOn)
         self.createPagingBlock()
   }
   this.xmlLoader = new dtmlXMLLoaderObject(this.doLoadDetails,this,true,this.no_cashe);
   if (_isIE) this.preventIECashing(true);
   this.dragger=new dhtmlDragAndDropObject();

/*METHODS. SERVICE*/
      /**
      *   @desc: on scroll grid inner actions
      *   @type: private
      *   @topic: 7
      */
      this._doOnScroll = function(e,mode){
		this.callEvent("onScroll",[this.objBox.scrollLeft,this.objBox.scrollTop]);
		this.doOnScroll(e,mode);
	}
      /**
      *   @desc: on scroll grid more inner action
      *   @type: private
      *   @topic: 7
      */
      this.doOnScroll = function(e,mode){
                  this.hdrBox.scrollLeft = this.objBox.scrollLeft;
              if (this.ftr)
                 this.ftr.parentNode.scrollLeft = this.objBox.scrollLeft;
                  this.setSortImgPos(null,true);
                        if (mode) return;
                  
                  //load more rows on scroll
                  if(!this.pagingOn && this.objBox.scrollTop+this.hdrSizeA+this.objBox.offsetHeight>this.objBox.scrollHeight){
                     if(this._xml_ready && (this.objBox._oldScrollTop!=this.objBox.scrollTop) && this.addRowsFromBuffer()){
                        this.objBox.scrollTop = this.objBox.scrollHeight - (this.hdrSizeA+1+this.objBox.offsetHeight)
                  this.objBox._oldScrollTop=this.objBox.scrollTop;
                  }
                  }

                        if (this._dload){
                        if (this._dLoadTimer)  window.clearTimeout(this._dLoadTimer);
                        this._dLoadTimer=window.setTimeout(function(){ if (self.limit) self._askRealRows(); },500);
                        }
               }
      /**
      *    @desc: attach grid to some object in DOM
      *    @param: obj - object to attach to
      *   @type: public
      *   @topic: 0,7
      */
      this.attachToObject = function(obj){
                        obj.appendChild(this.entBox)
                        this.objBox.style.height = this.entBox.style.height;

                     }
      /**
      *   @desc: initialize grid
      *   @param: fl - if to parse on page xml data island 
      *   @type: public
      *   @topic: 0,7
      */
      this.init =    function(fl){

	  				 if ((this.isTreeGrid()) && (!this._h2)){
						this._aEx=new _dhtmlxArray();
						this._h2=new dhtmlxHierarchy();
						if ((this._fake)&&(!this._realfake)) this._fake._h2=this._h2;
						this._tgc={imgURL:null};
	   				}
if(!this._hstyles) return;
                     this.editStop()
                     /*TEMPORARY STATES*/
                     this.lastClicked = null;//row clicked without shift key. used in multiselect only
                     this.resized = null;//hdr cell that is resized now
                     this.fldSorted = this.r_fldSorted = null;//hdr cell last sorted
                     this.gridWidth = 0;
                     this.gridHeight = 0;
                     //empty grid if it already was initialized
                     this.cellWidthPX = new Array(0);
                     this.cellWidthPC = new Array(0);
                     if(this.hdr.rows.length>0){
                        this.clearAll(true);
                     }
                     if(this.cellType._dhx_find("tree")!=-1){//create hashtable for treegrid
                        this.loadedKidsHash = new Hashtable();
                        this.loadedKidsHash.put("hashOfParents",new Hashtable())
                     }

                     var hdrRow = this.hdr.insertRow(0);
                            for(var i=0;i<this.hdrLabels.length;i++){
                                hdrRow.appendChild(document.createElement("TH"));
                                hdrRow.childNodes[i]._cellIndex=i;
                        hdrRow.childNodes[i].style.height="0px";
                                }
                            if (_isIE) hdrRow.style.position="absolute";
                            else  hdrRow.style.height='auto';

                     var hdrRow = this.hdr.insertRow(_isKHTML?2:1);

                            hdrRow._childIndexes=new Array();
                            var col_ex=0;
                     for(var i=0;i<this.hdrLabels.length;i++){
                                hdrRow._childIndexes[i]=i-col_ex;

                            if ((this.hdrLabels[i]==this.splitSign)&&(i!=0)){
                        if (_isKHTML)
                           hdrRow.insertCell(i-col_ex);
                                hdrRow.cells[i-col_ex-1].colSpan=(hdrRow.cells[i-col_ex-1].colSpan||1)+1;
                                hdrRow.childNodes[i-col_ex-1]._cellIndex++;
                                col_ex++;
                                hdrRow._childIndexes[i]=i-col_ex;
                                continue;
                                }

                     hdrRow.insertCell(i-col_ex);

                            hdrRow.childNodes[i-col_ex]._cellIndex=i;
                            hdrRow.childNodes[i-col_ex]._cellIndexS=i;
                           this.setHeaderCol(i,this.hdrLabels[i]);
                        }
                  if (col_ex==0) hdrRow._childIndexes=null;
                  this._cCount=this.hdrLabels.length;
	
                  if (_isIE) window.setTimeout(function(){ self.setSizes(); },1);

//create virtual top row
                                if (!this.obj.firstChild)
                                    this.obj.appendChild(document.createElement("TBODY"));

                                var tar=this.obj.firstChild;
                        if (!tar.firstChild){
                                    tar.appendChild(document.createElement("TR"));
                                    tar=tar.firstChild;
                                    if (_isIE) tar.style.position="absolute";
                                    else tar.style.height='auto';

                                   for(var i=0;i<this.hdrLabels.length;i++){
                                       tar.appendChild(document.createElement("TH"));
                              tar.childNodes[i].style.height="0px";
                              }
                        }


                     this.setColumnIds()
                	 this._c_order=null;
                     if(this.multiLine==-1)
                        this.multiLine = true;
                     if(this.multiLine != true)
                        this.obj.className+=" row20px";

                     //
                     //this.combos = new Array(this.hdrLabels.length);
                     //set sort image to initial state
                     this.sortImg.style.position = "absolute";
                     this.sortImg.style.display = "none";
                     this.sortImg.src = this.imgURL+"sort_desc.gif";
                     this.sortImg.defLeft = 0;
                     //create and kill a row to set initial size
                     //this.addRow("deletethisrtowafterresize",new Array("",""))
                     this.entCnt.rows[0].style.display = ''//display header
                     if(this.noHeader){
                        this.entCnt.rows[0].style.display = 'none';
                     }else{
                        this.noHeader = false
                     }

//#__pro_feature:21092006{
//#column_hidden:21092006{
                 if (this._ivizcol)   this.setColHidden();
//#}
//#}


                this.attachHeader();
                this.attachHeader(0,0,"_aFoot");
                this.setSizes();
                     if(fl)
                        this.parseXML()
                     this.obj.scrollTop = 0

                            if (this.dragAndDropOff)  this.dragger.addDragLanding(this.entBox,this);
                            if (this._initDrF) this._initD();
					if (this._init_point) this._init_point();
                  };
      /**
      *    @desc: sets sizes of grid elements
      *   @type: private
      *   @topic: 0,7
      */
      this.setSizes  =    function(fl){ 
	  				 if ((!this.hdr.rows[0])) return;
                     if (!this.entBox.offsetWidth) {
					 	if (this._sizeTime)
							window.clearTimeout(this._sizeTime);
							this._sizeTime=window.setTimeout(function(){ self.setSizes()},250);
					 	return;
					 }
			   		if (((_isFF)&&(this.entBox.style.height=="100%"))||(this._fixLater)){
						this.entBox.style.height=this.entBox.parentNode.clientHeight;
						this._fixLater=true;
					}

                     if(fl && this.gridWidth==this.entBox.offsetWidth && this.gridHeight==this.entBox.offsetHeight){
                        return false
                     }else if(fl){
                        this.gridWidth = this.entBox.offsetWidth
                        this.gridHeight = this.entBox.offsetHeight
                     }





                            if ((!this.hdrBox.offsetHeight)&&(this.hdrBox.offsetHeight>0))
                         this.entCnt.rows[0].cells[0].height = this.hdrBox.offsetHeight+"px";

                     var gridWidth = parseInt(this.entBox.offsetWidth)-(this._gcCorr||0);
                     var gridHeight = parseInt(this.entBox.offsetHeight)-((!_isIE)?(this._sizeFix||0):0);



                     var _isVSroll=(this.objBox.scrollHeight>this.objBox.offsetHeight);
                     if (((!this._ahgr)&&(_isVSroll))||((this._ahgrM)&&(this._ahgrM<this.objBox.scrollHeight)))
                                gridWidth-=(this._scrFix||(_isFF?17:17));





                     var len = this.hdr.rows[0].cells.length
//                var pcx_widht=(this._fake?(gridWidth-this._fake.entBox.offsetWidth):gridWidth);

                     for(var i=0;i<this._cCount;i++){
                        if(this.cellWidthType=='px' && this.cellWidthPX.length < len){
                           this.cellWidthPX[i] = this.initCellWidth[i] - this._wcorr;
                        }else if(this.cellWidthType=='%' && this.cellWidthPC.length < len){
                           this.cellWidthPC[i] = this.initCellWidth[i];
                        }
                        if(this.cellWidthType=='%' && this.cellWidthPC.length!=0 && this.cellWidthPC[i]){
                           this.cellWidthPX[i] = parseInt(gridWidth*this.cellWidthPC[i]/100);
                        }
                     }

                    var wcor=this.entBox.offsetWidth-this.entBox.clientWidth;

                    var summ = 0;
                	var fcols=new Array();

                     for(var i=0;i<this._cCount;i++)
                   if ((this.initCellWidth[i]=="*")&&((!this._hrrar)||(!this._hrrar[i])))
                           fcols[fcols.length]=i;
                  else
                           summ += parseInt(this.cellWidthPX[i]);
                if (fcols.length){
                   var ms=Math.floor((gridWidth-summ-wcor)/fcols.length);
                  if (ms<0) ms=1;
                   for(var i=0;i<fcols.length; i++){
                     var min=(this._drsclmW?this._drsclmW[fcols[i]]:0);
                           this.cellWidthPX[fcols[i]]=(min?(min>ms?min:ms):ms)-this._wcorr;
                     summ+=ms;
                     }
                }

                     var summ = 0;
                     for(var i=0;i<this._cCount;i++)
                        summ += parseInt(this.cellWidthPX[i])
                   if (_isOpera) summ-=1;
                   
                this.chngCellWidth();
                if ((this._awdth)&&(this._awdth[0])){
                	//convert percents to PX
                	if (this.cellWidthType=='%') {
                			this.cellWidthType="px";
                			this.cellWidthPC=[];
            			}
                	var gs=(summ>this._awdth[1]?this._awdth[1]:(summ<this._awdth[2]?this._awdth[2]:summ)); 
                	this.entBox.style.width=gs+((_isVSroll && !this._ahgr)?(_isFF?20:18):0)+"px";
            	}                   

                       this.objBuf.style.width = summ + "px";
                  if ((this.ftr)&&(!this._realfake))
                       this.ftr.style.width = summ + "px";

                       this.objBuf.childNodes[0].style.width = summ + "px";
                            //if (_isOpera) this.hdr.style.width = summ + this.cellWidthPX.length*2 + "px";
                     //set auto page size of dyn scroll
                     this.doOnScroll(0,1);

                     //set header part of container visible height to header's height
                     //this.entCnt.rows[0].cells[0].style.height = this.hdr.offsetHeight;

                                 this.hdr.style.border="0px solid gray";  //FF 1.0 fix
/*                         if ((_isMacOS)&&(_isFF))
                                    var zheight=20;
                                 else*/
                                var zheight=this.hdr.offsetHeight+(this._borderFix?this._borderFix:0);
				                if (this.ftr) zheight+=this.ftr.offsetHeight;

                                if (this._ahgr)
                                    if (this.objBox.scrollHeight){
                                        if (_isIE)
                                            var z2=this.objBox.scrollHeight;
                                        else
                                            var z2=this.objBox.childNodes[0].scrollHeight;
                                       var scrfix=this.parentGrid?1:((this.objBox.offsetWidth<this.objBox.scrollWidth)?(_isFF?20:18):1);
                              if (this._ahgrMA)
                                 z2=this.entBox.parentNode.offsetHeight-zheight-scrfix-(this._sizeFix?this._sizeFix:0)*2;


                                 if (((this._ahgrM)&&((this._ahgrF?(z2+zheight+scrfix):z2)>this._ahgrM)))
                                              gridHeight=this._ahgrM*1+(this._ahgrF?0:(zheight+scrfix));
                                 else
                                    gridHeight=z2+zheight+scrfix;

                                        this.entBox.style.height=gridHeight+"px";
                                  }

				                if (this.ftr) zheight-=this.ftr.offsetHeight;

                var aRow=this.entCnt.rows[1].cells[0].childNodes[0];
               
                if(!this.noHeader)
                     aRow.style.top = (zheight-this.hdrBox.offsetHeight+((_isIE && !window.XMLHttpRequest)?(-wcor):0) )+"px";
                if (this._topMb) {
                	this._topMb.style.top=(zheight||0)+"px";
					this._topMb.style.width=(gridWidth+20)+"px";
            	}
				if (this._botMb) {
					this._botMb.style.top=(gridHeight-3)+"px";
					this._botMb.style.width=(gridWidth+20)+"px";					
				}

                     //nb 072006:
                     aRow.style.height = (((gridHeight - zheight-1)<0 && _isIE)?20:(gridHeight - zheight-1))-(this.ftr?this.ftr.offsetHeight:0)+"px";
                if (this.ftr && this.entBox.offsetHeight>this.ftr.offsetHeight) this.entCnt.style.height=this.entBox.offsetHeight-this.ftr.offsetHeight+"px";

                            if (this._dload)
                                this._dloadSize=Math.floor(parseInt(this.entBox.offsetHeight)/20)+(_isKHTML?4:2); //rough, but will work

                  };

      /**
      *   @desc: changes cell width
      *   @param: [ind] - index of row in grid
      *   @type: private
      *   @topic: 4,7
      */
      this.chngCellWidth = function(){
                       if ((_isOpera)&&(this.ftr))
                           this.ftr.width=this.objBox.scrollWidth+"px";
                     var l=this._cCount;
                           for(var i=0;i<l;i++){
                              this.hdr.rows[0].cells[i].style.width = this.cellWidthPX[i]+"px";
                              this.obj.rows[0].childNodes[i].style.width = this.cellWidthPX[i]+"px";
                       if (this.ftr)
                                 this.ftr.rows[0].cells[i].style.width = this.cellWidthPX[i]+"px";
                           }
                        }
      /**
      *   @desc: set delimiter character used in list values (default is ",")
      *   @param: delim - delimiter as string
      *   @before_init: 1
      *   @type: public
      *   @topic: 0
      */
      this.setDelimiter = function(delim){
         this.delim = delim;
      }
      /**
      *   @desc: set width of columns in percents
      *   @type: public
      *   @before_init: 1
      *   @param: wp - list of column width in percents
      *   @topic: 0,7
      */
      this.setInitWidthsP = function(wp){
         this.cellWidthType = "%";
         this.initCellWidth = wp.split(this.delim.replace(/px/gi,""));
         this._setAutoResize();
      }
      /**
	  *	@desc:
	  *	@type: private
	  *	@topic: 0
	  */
      this._setAutoResize=function(){
            var el=window;
            var self=this;
           
            if(el.addEventListener){
                if ((_isFF)&&(_FFrv<1.8))
                    el.addEventListener("resize",function (){
                        if (!self.entBox) return;
                        var z=self.entBox.style.width;
                        self.entBox.style.width="1px";

                        window.setTimeout(function(){ self.entBox.style.width=z; self.setSizes();  if (self._fake) self._fake._correctSplit(); },10);
                        },false);
                else
                    el.addEventListener("resize",function (){ if (self.setSizes) self.setSizes(); if (self._fake) self._fake._correctSplit();  },false);
                }
            else if (el.attachEvent)
                el.attachEvent("onresize",function(){ 
                    if (self._resize_timer) window.clearTimeout(self._resize_timer);
                    if (self.setSizes)
                        self._resize_timer=window.setTimeout(function(){ self.setSizes();  if (self._fake) self._fake._correctSplit(); },500);
                });
            this._setAutoResize=function(){};   	
      }
      /**
      *   @desc: set width of columns in pixels
      *   @type: public
      *   @before_init: 1
      *   @param: wp - list of column width in pixels
      *   @topic: 0,7
      */
      this.setInitWidths = function(wp){
         this.cellWidthType = "px";
         this.initCellWidth = wp.split(this.delim);
            if (_isFF){
                for (var i=0; i<this.initCellWidth.length; i++)
               if (this.initCellWidth[i]!="*")
                    this.initCellWidth[i]=parseInt(this.initCellWidth[i])-2;
            }

      }

      /**
      *   @desc: set multiline rows support to enabled or disabled state
      *   @type: public
      *   @before_init: 1
      *   @param: state - true or false
      *   @topic: 0,7
      */
      this.enableMultiline = function(state){
         this.multiLine = convertStringToBoolean(state);
      }

      /**
      *   @desc: set multiselect mode to enabled or disabled state
      *   @type: public
      *   @param: state - true or false
      *   @topic: 0,7
      */
      this.enableMultiselect = function(state){
         this.selMultiRows = convertStringToBoolean(state);
      }

      /**
      *   @desc: set path to grid internal images (sort direction, any images used in editors, checkbox, radiobutton)
      *   @type: public
      *   @param: path - url (or relative path) of images folder with closing "/"
      *   @topic: 0,7
      */
      this.setImagePath = function(path){
         this.imgURL = path;
      }

      /**
      *   @desc: part of column resize routine
      *   @type: private
      *   @param: ev - event
      *   @topic: 3
      */
      this.changeCursorState = function (ev){
                           var el = ev.target||ev.srcElement;
                     if(el.tagName!="TD")
                           el = this.getFirstParentOfType(el,"TD")
                           if ((el.tagName=="TD")&&(this._drsclmn)&&(!this._drsclmn[el._cellIndex])) return  el.style.cursor = "default";
						   var check = ev.layerX+(((!_isIE)&&(ev.target.tagName=="DIV"))?el.offsetLeft:0);
                           if((el.offsetWidth - (ev.offsetX||(parseInt(this.getPosition(el,this.hdrBox))-check)*-1))<10){
                              el.style.cursor = "E-resize";
                           }else
                              el.style.cursor = "default";
                       if (_isOpera) this.hdrBox.scrollLeft = this.objBox.scrollLeft;
                        }
      /**
      *   @desc: part of column resize routine
      *   @type: private
      *   @param: ev - event
      *   @topic: 3
      */
      this.startColResize = function(ev){
                           this.resized = null;
                           var el = ev.target||ev.srcElement;
                     if(el.tagName!="TD")
                        el = this.getFirstParentOfType(el,"TD")
                           var x = ev.clientX;
                           var tabW = this.hdr.offsetWidth;
                           var startW = parseInt(el.offsetWidth)
                           if(el.tagName=="TD" && el.style.cursor!="default"){
                                        if ((this._drsclmn)&&(!this._drsclmn[el._cellIndex])) return;
                              this.entBox.onmousemove = function(e){this.grid.doColResize(e||window.event,el,startW,x,tabW)}
                              document.body.onmouseup = new Function("","document.getElementById('"+this.entBox.id+"').grid.stopColResize()");
                           } 
                        }
      /**
      *   @desc: part of column resize routine
      *   @type: private
      *   @param: ev - event
      *   @topic: 3
      */
      this.stopColResize = function(){
                           this.entBox.onmousemove = "";//removeEventListener("mousemove")//
                           document.body.onmouseup = "";
                           this.setSizes();
                           this.doOnScroll(0,1)
						   this.callEvent("onResizeEnd",[this]);
                        }
      /**
      *   @desc: part of column resize routine
      *   @param: el - element (column resizing)
      *   @param: startW - started width
      *   @param: x - x coordinate to resize from
      *   @param: tabW - started width of header table
      *   @type: private
      *   @topic: 3
      */
      this.doColResize = function(ev,el,startW,x,tabW){
                        el.style.cursor = "E-resize";
                        this.resized = el;
                        var fcolW = startW + (ev.clientX-x);
                        var wtabW = tabW + (ev.clientX-x)
                                if (!(this.callEvent("onResize",[el._cellIndex,fcolW,this]))) return;
                                if (el.colSpan>1){
                                    var a_sizes=new Array();
                                    for (var i=0; i<el.colSpan; i++)
                                         a_sizes[i]=Math.round(fcolW*this.hdr.rows[0].childNodes[el._cellIndexS+i].offsetWidth/el.offsetWidth);
                                    for (var i=0; i<el.colSpan; i++)
                                        this._setColumnSizeR(el._cellIndexS+i*1,a_sizes[i]);
                                }
                        else
                                this._setColumnSizeR(el._cellIndex,fcolW);
                                this.doOnScroll(0,1);
                              if (_isOpera) this.setSizes();
                              this.objBuf.childNodes[0].style.width = "";
                     }

      /**
      *   @desc: set width of grid columns ( zero row of header and body )
      *   @type: private
      *   @topic: 7
      */
       this._setColumnSizeR=function(ind, fcolW){
                        if(fcolW>((this._drsclmW  && !this._notresize)?(this._drsclmW[ind]||10):10)){
                           this.obj.firstChild.firstChild.childNodes[ind].style.width = fcolW+"px";
                           this.hdr.rows[0].childNodes[ind].style.width = fcolW+"px";
                     if (this.ftr)
                        this.ftr.rows[0].childNodes[ind].style.width = fcolW+"px";
                           if(this.cellWidthType=='px'){
                              this.cellWidthPX[ind]=fcolW;
                           }else{
                             var gridWidth = parseInt(this.entBox.offsetWidth);
                              if (this.objBox.scrollHeight>this.objBox.offsetHeight)
                          gridWidth-=(this._scrFix||(_isFF?17:17));
                              var pcWidth = Math.round(fcolW/gridWidth*100)
                              this.cellWidthPC[ind]=pcWidth;
                           }
                        }
         }
      /**
      *    @desc: sets position and visibility of sort arrow
      *    @param: state - true/false - show/hide image
      *    @param: ind - index of field
      *    @param: order - asc/desc - type of image
	  *    @param: row - one based index of header row ( used in multirow headers, top row by default )
      *   @type: public
      *   @topic: 7
      */
         this.setSortImgState=function(state,ind,order,row){
         	order=(order||"asc").toLowerCase();
            if (!convertStringToBoolean(state)){
             this.sortImg.style.display = "none";
             this.fldSorted=null;
                return;
                }

            if  (order=="asc")
             this.sortImg.src = this.imgURL+"sort_asc.gif";
            else
             this.sortImg.src = this.imgURL+"sort_desc.gif";
            this.sortImg.style.display="";
            this.fldSorted=this.hdr.rows[0].childNodes[ind];
            var r=this.hdr.rows[row||1];
            for (var i=0; i < r.childNodes.length; i++) 
            	if (r.childNodes[i]._cellIndex==ind)
	            	this.r_fldSorted=r.childNodes[i];
            		this.setSortImgPos();
        }

      /**
      *    @desc: sets position and visibility of sort arrow
      *    @param: ind - index of field
      *    @param: ind - index of field
      *    @param: hRowInd - index of row in case of complex header, one-based, optional

      *   @type: private
      *   @topic: 7
      */
      this.setSortImgPos = function(ind,mode,hRowInd,el){
              if (!el){
                           if(!ind)
                              var el = this.r_fldSorted;
                           else
                              var el = this.hdr.rows[hRowInd||0].cells[ind];
                     }

                           if(el!=null){
                              var pos = this.getPosition(el,this.hdrBox)
                              var wdth = el.offsetWidth;
                              this.sortImg.style.left = Number(pos[0]+wdth-13)+"px";//Number(pos[0]+5)+"px";
                              this.sortImg.defLeft = parseInt(this.sortImg.style.left)
                              this.sortImg.style.top = Number(pos[1]+5)+"px";

                              if ((!this.useImagesInHeader)&&(!mode))
                                 this.sortImg.style.display = "inline";
                              this.sortImg.style.left = this.sortImg.defLeft+"px";//-parseInt(this.hdrBox.scrollLeft)
                           }
                        }

      /**
      *   @desc: manage activity of the grid.
      *   @param: fl - true to activate,false to deactivate
      *   @type: private
      *   @topic: 1,7
      */
      this.setActive = function(fl){
                     if(arguments.length==0)
                        var fl = true;
                     if(fl==true){
                           //document.body.onkeydown = new Function("","document.getElementById('"+this.entBox.id+"').grid.doKey()")//
                   if (globalActiveDHTMLGridObject && ( globalActiveDHTMLGridObject != this ))
                     globalActiveDHTMLGridObject.editStop();

                        globalActiveDHTMLGridObject = this;
                        this.isActive = true;
                     }else{
                        this.isActive = false;
                     }
                  };
      /**
      *     @desc: called on click occured
      *     @type: private
      */
      this._doClick = function(ev){
                     var selMethod = 0;
                     var el = this.getFirstParentOfType(_isIE?ev.srcElement:ev.target,"TD");
                     var fl = true;
					 
					  //mm
					 //markers start
					 if(this.markedCells){
					 	var markMethod = 0;
						
					 	if(ev.shiftKey || ev.metaKey){
                           markMethod = 1;
                        }
                        if(ev.ctrlKey){
                           markMethod = 2;
                        }
						this.doMark(el,markMethod);
						return true;
					 } 
					 //markers end
					 //mm
					 
                     if(this.selMultiRows!=false){
                        if(ev.shiftKey && this.row!=null){
                           selMethod = 1;
                        }
                        if(ev.ctrlKey || ev.metaKey){
                           selMethod = 2;
                        }

                     }
                     this.doClick(el,fl,selMethod)
                  };


      /**
      *   @desc: called onmousedown inside grid area
      *   @type: private
      */
        this._doContClick=function(ev){
                     var el = this.getFirstParentOfType(_isIE?ev.srcElement:ev.target,"TD");
                            if ((!el)||(typeof(el.parentNode.idd)=="undefined")) return true;
                            if (ev.button==2 || (_isMacOS && ev.ctrlKey)){
                        if (!this.callEvent("onRightClick",[el.parentNode.idd,el._cellIndex,ev])) {
                           var z=function(e){ document.body.oncontextmenu=Function("return true;"); (e||event).cancelBubble=true; return false; }
                           if (_isIE) ev.srcElement.oncontextmenu=z;
                              else if (!_isMacOS) document.body.oncontextmenu=z;

                           return false;
                        }
                        if (this._ctmndx){
                                   if (!(this.callEvent("onBeforeContextMenu",[el.parentNode.idd,el._cellIndex,this]))) return true;
                                   el.contextMenuId=el.parentNode.idd+"_"+el._cellIndex;
                                   el.contextMenu=this._ctmndx;
                                   el.a=this._ctmndx._contextStart;
                                   if (_isIE)
                                       ev.srcElement.oncontextmenu = function(){ event.cancelBubble=true; return false; };
                                   el.a(el,ev);
                                   el.a=null;
                           }
                            }
                     else
                        if(this._ctmndx) this._ctmndx._contextEnd();
            return true;
        }

      /**
      *    @desc: occures on cell click (supports treegrid)
      *   @param: [el] - cell to click on
      *   @param:   [fl] - true if to call onRowSelect function
      *   @param: [selMethod] - 0 - simple click, 1 - shift, 2 - ctrl
      *   @param: show - true/false - scroll row to view, true by defaul    
      *   @type: private
      *   @topic: 1,2,4,9
      */
      this.doClick = function(el,fl,selMethod,show){ 

	  			if(this.markedCells){ return true;}//mm: markers
		
                  var psid=this.row?this.row.idd:0;

                     this.setActive(true);
                     if(!selMethod)
                        selMethod = 0;
                     if(this.cell!=null)
                        this.cell.className = this.cell.className.replace(/cellselected/g,"");
                     if(el.tagName=="TD" && (this.rowsCol._dhx_find(this.rowsAr[el.parentNode.idd])!=-1 || this.rowsBuffer[0]._dhx_find(el.parentNode.idd)!=-1 || this.isTreeGrid())){
                        if (this.checkEvent("onSelectStateChanged")) var initial=this.getSelectedId();
                  var prow=this.row;
                        if(selMethod==0){
                           this.clearSelection();
                        }else if(selMethod==1){
                           var elRowIndex = this.rowsCol._dhx_find(el.parentNode)
                           var lcRowIndex = this.rowsCol._dhx_find(this.lastClicked)
                           if(elRowIndex>lcRowIndex){
                              var strt = lcRowIndex;
                              var end = elRowIndex;
                           }else{
                              var strt = elRowIndex;
                              var end = lcRowIndex;
                           }
                           for(var i=0;i<this.rowsCol.length;i++)
                              if((i>=strt && i<=end)){
                              	if (this.rowsCol[i] && (!this.rowsCol[i]._sRow)){
                              	  
                         		  if (this.rowsCol[i].className.indexOf("rowselected")==-1 && this.callEvent("onBeforeSelect",[this.rowsCol[i].idd,psid])){
                                    this.rowsCol[i].className+=" rowselected";
                                    this.selectedRows[this.selectedRows.length] = this.rowsCol[i]
		                        }}
		                        else{
		                        	this.clearSelection();
		                        	return this.doClick(el,fl,0,show);
		                        }
							  }	                    	
                              
                        }else if(selMethod==2){
                           if(el.parentNode.className.indexOf("rowselected") != -1){
                              el.parentNode.className=el.parentNode.className.replace(/rowselected/g,"");
                              this.selectedRows._dhx_removeAt(this.selectedRows._dhx_find(el.parentNode))
                              var skipRowSelection = true;
                           }
                        }
                        this.editStop()
                        this.cell = el;

                        if ((prow == el.parentNode)&&(this._chRRS))
                     fl=false;

						if (typeof(el.parentNode.idd)=="undefined") return true;
                        this.row = el.parentNode;

                        if((!skipRowSelection)&&(!this.row._sRow)){
                     if (this.callEvent("onBeforeSelect",[this.row.idd,psid])){
                              this.row.className+= " rowselected"
                              if(this.selectedRows._dhx_find(this.row)==-1)
                                 this.selectedRows[this.selectedRows.length] = this.row;
                     }
                     else this.row=prow;

                        }
                        if(this.selBasedOn=="cell"){
                           if (this.cell.parentNode.className.indexOf("rowselected")!=-1)
                               this.cell.className = this.cell.className.replace(/cellselected/g,"")+" cellselected";
                        }

                  if(selMethod!=1)
                  		if (!this.row) return;
                        this.lastClicked = el.parentNode;
						
                        var rid = this.row.idd;
                        var cid = this.cell._cellIndex;
                        if (fl && typeof(rid)!="undefined") self.onRowSelectTime=setTimeout(function(){ self.callEvent("onRowSelect",[rid,cid]); },100)
                        if (this.checkEvent("onSelectStateChanged")) {
                            var afinal=this.getSelectedId();
                            if (initial!=afinal)  this.callEvent("onSelectStateChanged",[afinal]);
                        }
                     }
                     this.isActive = true;
                     if (show!==false)
                     this.moveToVisible(this.cell)
                  }

      /**
      *   @desc: select all rows in grid, it doesn't fire any events
      *   @param: edit - switch selected cell to edit mode
      *   @type: public
      *   @topic: 1,4
      */
      this.selectAll = function(){
      		this.clearSelection();
      		this.selectedRows=dhtmlxArray([].concat(this.rowsCol));
      		if (this.selectedRows.length){
	      		this.row=this.selectedRows[0];
	      		this.cell=this.row.cells[0];
      		}
      		for (var i=0; i<this.rowsCol.length; i++)
      			this.rowsCol[i].className+=" rowselected";
      		if ((this._fake)&&(!this._realfake)) this._fake.selectAll();
      		
  	}
      /**
      *   @desc: set selection to specified row-cell
      *   @param: r - row object or row index
      *   @param: cInd - cell index
      *   @param: [fl] - true if to call onRowSelect function
        *   @param: preserve - preserve previously selected rows true/false (false by default)
        *   @param: edit - switch selected cell to edit mode
	  *   @param: show - true/false - scroll row to view, true by defaul         
      *   @type: public
      *   @topic: 1,4
      */
      this.selectCell = function(r,cInd,fl,preserve,edit,show){
                     if(!fl)
                        fl = false;
                     if(typeof(r)!="object")
                        r = this.rowsCol[r]
//#__pro_feature:21092006{
//#colspan:20092006{
                            if (r._childIndexes)
                         var c = r.childNodes[r._childIndexes[cInd]];
                            else
//#}
//#}
                         var c = r.childNodes[cInd];
                         if (!c) c=r.childNodes[0];
                            if (preserve)
                         this.doClick(c,fl,3,show)
                            else
                         this.doClick(c,fl,0,show)
                            if (edit) this.editCell();
                  }
      /**
      *   @desc: moves specified cell to visible area (scrolls)
      *   @param: cell_obj - object of the cell to work with
      *   @param: onlyVScroll - allow only vertical positioning

      *   @type: private
      *   @topic: 2,4,7
      */
      this.moveToVisible = function(cell_obj,onlyVScroll){
                     try{
                        var distance = cell_obj.offsetLeft+cell_obj.offsetWidth+20;

						var scrollLeft=0;
                        if(distance>(this.objBox.offsetWidth+this.objBox.scrollLeft)){
                        	if(cell_obj.offsetLeft>this.objBox.scrollLeft)
                           		scrollLeft = cell_obj.offsetLeft-5
                        }else if(cell_obj.offsetLeft<this.objBox.scrollLeft){
                        	if(distance<this.objBox.scrollLeft)
                           		scrollLeft =  cell_obj.offsetLeft-5
                        }
                        if ((scrollLeft)&&(!onlyVScroll))
                           this.objBox.scrollLeft = scrollLeft;

                        var distance = cell_obj.offsetTop+cell_obj.offsetHeight + 20;
                        if(distance>(this.objBox.offsetHeight+this.objBox.scrollTop)){
                           var scrollTop = distance - this.objBox.offsetHeight;
                        }else if(cell_obj.offsetTop<this.objBox.scrollTop){
                           var scrollTop =  cell_obj.offsetTop-5
                        }
                        if(scrollTop)
                           this.objBox.scrollTop = scrollTop;
                                          }catch(er){
                     }
                  }
      /**
      *   @desc: creates Editor object and switch cell to edit mode if allowed
      *   @type: public
      *   @topic: 4
      */
      this.editCell = function(){ 
                     this.editStop();
                     if ((this.isEditable!=true)||(!this.cell))
                        return false;
                     var c = this.cell;
                            //#locked_row:11052006{
                            if (c.parentNode._locked) return false;
                            //#}

                this.editor = this.cells4(c);

                     //initialize editor
                     if(this.editor!=null){
                           if (this.editor.isDisabled()) { this.editor=null; return false; }
                           if(this.callEvent("onEditCell",[0,this.row.idd,this.cell._cellIndex])!=false && this.editor.edit){
                              this._Opera_stop=(new Date).valueOf();
                              c.className+=" editable";
                              this.editor.edit();
                              this.callEvent("onEditCell",[1,this.row.idd,this.cell._cellIndex])
                           }else{//preserve editing
                              this.editor=null;
                           }
                     }
                  }
      /**
      *   @desc: retuns value from editor(if presents) to cell and closes editor
      *   @mode: if true - current edit value will be reverted to previous one
      *   @type: public
      *   @topic: 4
      */
      this.editStop = function(mode){
                       if (_isOpera)
                                if (this._Opera_stop){
                                    if ((this._Opera_stop*1+50)>(new Date).valueOf()) return;
                                    this._Opera_stop=null;
                                }

                    if(this.editor && this.editor!=null){
                       this.editor.cell.className=this.editor.cell.className.replace("editable","");
                    if (mode){
                    	var t=this.editor.val;
                    	this.editor.detach();
                    	this.editor.setValue(t);
                    	this.editor=null;
                    	return;
                    }
                    if (this.editor.detach()) this.cell.wasChanged = true;

               var g=this.editor;
                    this.editor=null;
                    var z=this.callEvent("onEditCell",[2,this.row.idd,this.cell._cellIndex,g.getValue(),g.val]);

               if ((typeof(z)=="string")||(typeof(z)=="number"))
				  g[g.setImage?"setLabel":"setValue"](z);
               else
				  if (!z) g[g.setImage?"setLabel":"setValue"](g.val);
                     }
                  }
	/**
	*	@desc: 
	*	@type: private
	*/
	this._nextRowCell=function(row,dir,pos){
		row=this._nextRow(this.rowsCol._dhx_find(row),dir);
		if (!row) return null;
			return row.childNodes[row._childIndexes?row._childIndexes[pos]:pos];
		}
	/**
	*	@desc: 
	*	@type: private
	*/
	this._getNextCell=function(acell,dir,i){
		
		
      	acell=acell||this.cell;
		
        var arow=acell.parentNode;
		if (this._tabOrder){
			i=this._tabOrder[acell._cellIndex];
		if (typeof i != "undefined")
		  	if (i < 0)
		  		 acell=this._nextRowCell(arow,dir,Math.abs(i)-1);
		  	else acell=arow.childNodes[i];
  		} else {
  			var i=acell._cellIndex+dir;
  			if (i >= 0 && i < this._cCount ){
  				if (arow._childIndexes) i=arow._childIndexes[acell._cellIndex]+dir;
  				acell=arow.childNodes[i];
  			}
  			else{
				
  				acell=this._nextRowCell(arow,dir,(dir==1?0:(this._cCount-1)));
  				
			}
  		}
		
		
		
		if (!acell){ 
			if( (dir == 1) && this.tabEnd){
				this.tabEnd.focus();
				this.tabEnd.focus();
			}
			if( (dir == -1) && this.tabStart){
				this.tabStart.focus();
				this.tabStart.focus();
			}
			return null;
		}
		//tab out
	
		// tab readonly 
		if (acell.style.display!="none" &&( !this.smartTabOrder || !this.cells(acell.parentNode.idd,acell._cellIndex).isDisabled() ))
        		return acell;
      	return this._getNextCell(acell,dir);
		// tab readonly 
		
   }
	/**
	*	@desc: 
	*	@type: private
	*/
	this._nextRow=function(ind,dir){
		var r=this.rowsCol[ind+dir];
		if (r && r.style.display=="none") return this._nextRow(ind+dir,dir);
		return r;	
	}
	/**
	*	@desc: 
	*	@type: private
	*/
	this.scrollPage = function(dir){                           
                        var new_ind=Math.floor((this.getRowIndex(this.row.idd)||0)+(dir)*this.objBox.offsetHeight/(this._srdh||20));
                        if (new_ind<0) new_ind=0;
                        if (this._dload && (!this.rowsCol[new_ind])){
                        	this._askRealRows(new_ind,function(){
                        			try{ self.selectCell(new_ind,(this.cell?this.cell._cellIndex:0),true); } catch(e){};
                        		});
	                        }
                        else{
                        	if (new_ind>=this.rowsCol.length) new_ind=this.rowsCol.length-1;
                               this.selectCell(new_ind,this.cell._cellIndex,true); 
                        }
	}	
	
      /**
      *   @desc: manages keybord activity in grid
      *   @type: private
      *   @topic: 7
      */
      this.doKey =   function(ev){
                            if (!ev) return true;
                            if ((ev.target||ev.srcElement).value!==window.undefined){
                                 var zx= (ev.target||ev.srcElement);
                                 if ((!zx.parentNode)||(zx.parentNode.className.indexOf("editable")==-1))
                                     return true;
                                 }
                            if ((globalActiveDHTMLGridObject)&&(this!=globalActiveDHTMLGridObject))
                                return globalActiveDHTMLGridObject.doKey(ev);
                     if(this.isActive==false){
                        //document.body.onkeydown = "";
                        return true;
                     }

                     if (this._htkebl) return true;
                     if (!this.callEvent("onKeyPress",[ev.keyCode,ev.ctrlKey,ev.shiftKey,ev])) return false;
					 
                     var code="k"+ev.keyCode+"_"+(ev.ctrlKey?1:0)+"_"+(ev.shiftKey?1:0);
                     if (this.cell){ //if selection exists in grid only
                     	if (this._key_events[code]){
                     		if (false===this._key_events[code].call(this)) return true;
                     		if (ev.preventDefault) ev.preventDefault();		
                     		ev.cancelBubble=true;
                     		return false;
                 		}
                 	
                 		if (this._key_events["k_other"])
                 			this._key_events.k_other.call(this,ev);
				     }
                 		
                 	
                    return true;
                  }
   /**
   *   @desc: selects row (?)for comtatibility with previous version
   *   @param: cell - cell object(or cell's child)
   *   @invoke: click on cell(or cell content)
   *   @type: private
   *   @topic: 1,2
   */
   this.getRow = function(cell){
                  if(!cell)
                     cell = window.event.srcElement;
                  if(cell.tagName!='TD')
                     cell = cell.parentElement;
                  r = cell.parentElement;
                  if(this.cellType[cell._cellIndex]=='lk')
                     eval(this.onLink+"('"+this.getRowId(r.rowIndex)+"',"+cell._cellIndex+")");
                  this.selectCell(r,cell._cellIndex,true)
               }
   /**
   *   @desc: selects row (and first cell of it)
   *   @param: r - row index or row object
   *   @param: fl - if true, then call function on select
    *   @param: preserve - preserve previously selected rows true/false (false by default)
	*   @param: show - true/false - scroll row to view, true by defaul    
   *   @type: public
   *   @topic: 1,2
   */
   this.selectRow = function(r,fl,preserve,show){
                  if(typeof(r)!='object')
                     r = this.rowsCol[r]
                  this.selectCell(r,0,fl,preserve,false,show)
               };
   /**
   *   @desc: sorts rows by specified column
   *   @param: col - column index
   *   @param:   type - str.int.date
   *   @param: order - asc,desc
   *   @type: public
   *   @topic: 2,3,5,9
   */
   this.sortRows = function(col,type,order){
   				  order=(order||"asc").toLowerCase();
   				  type=(type||this.fldSort[col]);
                  while(this.addRowsFromBuffer(true));//nb:paging - before sorting put all rows from buffer to rows collection.
                  //if tree cell exists
                  if(this.cellType._dhx_find("tree")!=-1){ 
                     return this.sortTreeRows(col,type,order)
                  }
                        var self=this;
                        var arrTS=new Array();
                        var atype = this.cellType[col];
                  var amet="getValue";
                  if (atype=="link")  amet="getContent";
                  if (atype=="dhxCalendar" || atype=="dhxCalendarA")  amet="getDate";


                        for (var i=0; i<this.rowsCol.length; i++)
                                 arrTS[this.rowsCol[i].idd]=this.cells3(this.rowsCol[i],col)[amet]();

                        this._sortRows(col,type,order,arrTS);
               }
	/**
	*	@desc: 
	*	@type: private
	*/
	this._sortCore=function(col,type,order,arrTS,s){
				var sort="sort";
                if (this._sst)  {
                	s["stablesort"]=this.rowsCol.stablesort;
                	sort="stablesort";
                }
                
//#__pro_feature:21092006{
//#custom_sort:21092006{
			 if(type.length>4) type=window[type];
			 
             if(type=='cus'){
             s[sort](function(a,b){
				return self._customSorts[col](arrTS[a.idd],arrTS[b.idd],order,a.idd,b.idd);
             });
             }else if(typeof(type)=='function'){
             s[sort](function(a,b){
				return type(arrTS[a.idd],arrTS[b.idd],order,a.idd,b.idd);
             });
         	 } else
//#}
//#}
             if(type=='str'){
             s[sort](function(a,b){
             if(order=="asc")
                  return arrTS[a.idd]>arrTS[b.idd]?1:-1
             else
                  return arrTS[a.idd]<arrTS[b.idd]?1:-1
             });
             }else if(type=='int'){
             s[sort](function(a,b){
             var aVal = parseFloat(arrTS[a.idd]); aVal=isNaN(aVal)?-99999999999999:aVal;
             var bVal = parseFloat(arrTS[b.idd]); bVal=isNaN(bVal)?-99999999999999:bVal;
             if(order=="asc")
                  return aVal-bVal;
             else
                  return bVal-aVal;
             });
             }else if(type=='date'){
             s[sort](function(a,b){
             var aVal = Date.parse(arrTS[a.idd])||(Date.parse("01/01/1900"));
             var bVal = Date.parse(arrTS[b.idd])||(Date.parse("01/01/1900"));
             if(order=="asc")
                return aVal-bVal
             else
                return bVal-aVal
             });
          }
                  
	}
      /**
      *   @desc: inner sorting routine
      *   @type: private
      *   @topic: 7
      */
    this._sortRows = function(col,type,order,arrTS){
                  
				  this._sortCore(col,type,order,arrTS,this.rowsCol);

                  if(this.pagingOn){//nb:paging
                       this.changePage(this.currentPage);
                       this.callEvent("onGridReconstructed",[]);
                  }else{
				    
					var tb = (_isKHTML)?this.obj:this.obj.rows[0].parentNode;
					for(var i=0;i<this.rowsCol.length;i++){
                       if  (this.rowsCol[i]!=this.obj._rows(i))
                           tb.insertBefore(this.rowsCol[i],this.obj._rows(i))
                     }
                  }
                       //this.setSizes()
                       this.callEvent("onGridReconstructed",[]);
}


   /**
   *   @desc: enables the possibility to load content from server when already loaded content was rendered. Using this feature you decrease the grid loading time for extremely big amounts of data ( in case of latest grid version, usage of SmartRendering instead of this mode strongly recommended )
   *   @param: filePath - path which will be used for fetching additional data
   *   @param: bufferSize - size of client size buffer 
   *   @type: public
   *   @topic: 0,7
   */
   this.setXMLAutoLoading = function(filePath,bufferSize){
        if (arguments.length==0) return (this._xmlaR=true);
      this.recordsNoMore = false;
      this.xmlFileUrl = filePath;
      this.rowsBufferOutSize = bufferSize||(this.rowsBufferOutSize==0?40:this.rowsBufferOutSize);
   }

   /**
   *   @desc: enables buffering in content rendering. Using this you decrease the grid loading time.
   *   @type: public
   *   @topic: 0,7
   */
   this.enableBuffering = function(bufferSize){
      this.rowsBufferOutSize = bufferSize||(this.rowsBufferOutSize==0?40:this.rowsBufferOutSize);
   }




   /**
   *   @desc: create rows from another part of buffer
   *   @type: private
   *   @topic: 0,2,7
   */
   this.addRowsFromBuffer = function(stopBeforeServerCall){
      if(this.rowsBuffer[0].length==0){
         if(!this.recordsNoMore && !stopBeforeServerCall){
         	if (this.limit && this.rowsCol.length>=this.limit) return false;
            if ((this.xmlFileUrl!="")&&(!this._startXMLLoading)){
                    this._startXMLLoading=true;
               this.loadXML(this.xmlFileUrl)
            }
         }else
            return false;
      }
      var cnt = Math.min(this.rowsBufferOutSize,this.rowsBuffer[0].length)


      //this.rowsBuffer.length
      for(var i=0;i<cnt;i++){
         //nb:newbuffer

         if(this.rowsBuffer[1][0].tagName == "TR"){//insert already created row
            this._insertRowAt(this.rowsBuffer[1][0],-1,this.pagingOn);
         }else{//create row from xml tag and insert it
            var rowNode = this.rowsBuffer[1][0]
			var r=this.createRowFromXMLTag(rowNode);
            this._insertRowAt(r,-1,this.pagingOn);
			this._postRowProcessing(r,rowNode);
         }
         this.rowsBuffer[0]._dhx_removeAt(0);
         this.rowsBuffer[1]._dhx_removeAt(0);
      }

      return this.rowsBuffer[0].length!=0;
   }
   /**
   *   @desc: creates row object based on xml tag
   *   @param: rowNode - object of xml tag "row"
   *   @type: private
   *   @returns: TR object
   */
   this.createRowFromXMLTag = function(rowNode){
      if(rowNode.tagName=="TR")//not xml tag, but already created TR
         return rowNode;

      var tree=this.cellType._dhx_find("tree");
      var rId = rowNode.getAttribute("id")

      this.rowsAr[rId] = this._prepareRow(rId);
      var r= this._fillRowFromXML(this.rowsAr[rId],rowNode,tree,null);
          
      return r;
   }

   /**
   *   @desc: allow multiselection
   *   @param: fl - false/true
   *   @type: deprecated
   *   @before_init: 1
   *   @topic: 0,2,7
   */
   this.setMultiselect = function(fl){
      this.selMultiRows = convertStringToBoolean(fl);
   }

   /**
   *   @desc: called when row was double clicked
   *   @type: private
   *   @topic: 1,2
   */
   this.wasDblClicked = function(ev){
      var el = this.getFirstParentOfType(_isIE?ev.srcElement:ev.target,"TD");
      if(el){
         var rowId = el.parentNode.idd;
         return this.callEvent("onRowDblClicked",[rowId,el._cellIndex]);
      }
   }

   /**
   *   @desc: called when header was clicked
   *   @type: private
   *   @topic: 1,2
   */
   this._onHeaderClick = function(e,el){
   	    var that=this.grid;
        el = el||that.getFirstParentOfType(_isIE?event.srcElement:e.target,"TD");
		if (this.grid.resized==null){
      		if (!(this.grid.callEvent("onHeaderClick",[el._cellIndexS,(e||window.event)]))) return false;
			that.sortField(el._cellIndexS,false,el)
		}
   }

   /**
   *   @desc: deletes selected row(s)
   *   @type: deprecated
   *   @topic: 2
   */
   this.deleteSelectedItem = function(){
   		this.deleteSelectedRows();
   }
   /**
   *   @desc: deletes selected row(s)
   *   @type: public
   *   @topic: 2
   */
   this.deleteSelectedRows = function(){
                     var num = this.selectedRows.length//this.obj.rows.length
                     if(num==0)
                        return;
                     var tmpAr = this.selectedRows;
                     this.selectedRows = new dhtmlxArray(0)
                     for(var i=num-1;i>=0;i--){
                        var node = tmpAr[i]

                                if(!this.deleteRow(node.idd,node)){
                           this.selectedRows[this.selectedRows.length] = node;
                        }else{
                           if(node==this.row){
                              var ind = i;
                           }
                        }
/*
                           this.rowsAr[node.idd] = null;
                           var posInCol = this.rowsCol._dhx_find(node)
                           this.rowsCol[posInCol].parentNode.removeChild(this.rowsCol[posInCol]);//nb:this.rowsCol[posInCol].removeNode(true);
                           this.rowsCol._dhx_removeAt(posInCol)*/
                     }
                     if(ind){
                        try{
                           if(ind+1>this.rowsCol.length)//this.obj.rows.length)
                              ind--;
                           this.selectCell(ind,0,true)
                        }catch(er){
                           this.row = null
                           this.cell = null
                        }
                     }
                  }

   /**
   *   @desc: gets selected row id
   *   @returns: id of selected row (list of ids with default delimiter) or null if non row selected
   *   @type: public
   *   @topic: 1,2,9
   */
   this.getSelectedRowId = function(){
   	return this.getSelectedId();
   }
   /**
   *   @desc: gets selected row id
   *   @returns: id of selected row (list of ids with default delimiter) or null if non row selected
   *   @type: deprecated
   *   @topic: 1,2,9
   */
   this.getSelectedId = function(){
                     var selAr = new Array(0); var uni={};
                     for(var i=0;i<this.selectedRows.length;i++){
                     	var id=this.selectedRows[i].idd;
                     	if (uni[id]) continue;
                        selAr[selAr.length]=id;
                        uni[id]=true;
                     }

                     //..
                     if(selAr.length==0)
                        return null;
                     else
                        return selAr.join(this.delim);
                  }
   /**
   *   @desc: gets index of selected cell
   *   @returns: index of selected cell or -1 if there is no selected sell
   *   @type: public
   *   @topic: 1,4
   */
   this.getSelectedCellIndex = function(){
                           if(this.cell!=null)
                              return this.cell._cellIndex;
                           else
                              return -1;
                        }
   /**
   *   @desc: gets width of specified column in pixels
   *   @param: ind - column index
   *   @returns: column width in pixels
   *   @type: public
   *   @topic: 3,7
   */
   this.getColWidth = function(ind){
                           return parseInt(this.cellWidthPX[ind])+((_isFF)?2:0);
                        }

   /**
   *   @desc: sets width of specified column in pixels (soen't works with procent based grid)
   *   @param: ind - column index
   *   @param: value - new width value
   *   @type: public
   *   @topic: 3,7
   */
   this.setColWidth = function(ind,value){
                        if (this.cellWidthType=='px')
                               this.cellWidthPX[ind]=parseInt(value);
                     else
                        this.cellWidthPC[ind]=parseInt(value);
                            this.setSizes();
                        }


   /**
   *   @desc: gets row object by id
   *   @param: id - row id
   *   @returns: row object or null if there is no row with specified id
   *   @type: private
   *   @topic: 2,7,9
   */
   this.getRowById = function(id){
                  var row = this.rowsAr[id]
                  if(row)
                     return row;
                  else
                     if (this._dload){
                         var ind = this.rowsBuffer[0]._dhx_find(id);
                         if (ind>=0) {
                               this._askRealRows(ind);
                                return this.getRowById(id);
                         }
                     }
                     else if(this.pagingOn){//use new buffer
                        var ind = this.rowsBuffer[0]._dhx_find(id);
                                if (ind>=0) {
                           var r = this.createRowFromXMLTag(this.rowsBuffer[1][ind]);
                           this._postRowProcessing(r,this.rowsBuffer[1][ind]);
                           this.rowsBuffer[1][ind] = r;
                           return r;
                        }else{
                           return null;
                        }
                     }
                else if (this._slowParse) //smart parsing mode in treegrid
                  return this._seekAndDeploy(id);
                  return null;
               }
   /**
   *   @desc: gets row by index from rowsCola and rowsBuffer
   *   @param: ind - row index
   *   @returns: row object
   *   @type: private
   */
   this.getRowByIndex = function(ind){
      if(this.rowsCol.length<=ind){
         if((this.rowsCol.length+this.rowsBuffer[0].length)<=ind)
            return null;
         else{
            var indInBuf = ind-this.rowsCol.length-1;
            var r = this.createRowFromXMLTag(this.rowsBuffer[1][indInBuf]);
            return r;
         }
      }else{
         return this.rowsCol[ind]
      }
   }

   /**
   *   @desc: gets row index by id (grid only)
   *   @param: row_id - row id
   *   @returns: row index or -1 if there is no row with specified id
   *   @type: public
   *   @topic: 2
   */
   this.getRowIndex = function(row_id){
                        var ind = this.rowsCol._dhx_find(this.getRowById(row_id));
                        if(ind!=-1)
                           return ind;
                        else{
                           ind = this.rowsBuffer[0]._dhx_find(row_id)
                           if(ind!=-1)
                              return ind+this.rowsCol.length;
                           return -1;
                        }
                  }
   /**
   *   @desc: gets row id by index
   *   @param: ind - row index
   *   @returns: row id or null if there is no row with specified index
   *   @type: public
   *   @topic: 2
   */
   this.getRowId = function(ind){
                            var z=this.rowsCol[parseInt(ind)];
                            if (z) return z.idd;
                            return (this.rowsBuffer[0][this._dload?ind:(ind-this.rowsCol.length)]||null);
                  }
   /**
   *   @desc: sets new id for row by its index
   *   @param: ind - row index
   *   @param: row_id - new row id
   *   @type: public
   *   @topic: 2
   */
   this.setRowId = function(ind,row_id){
                     var r = this.rowsCol[ind]
                     this.changeRowId(r.idd,row_id)
                  }
   /**
   *   @desc: changes id of the row to the new one
   *   @param: oldRowId - row id to change
   *   @param: newRowId - row id to set
   *   @type:public
   *   @topic: 2
   */
   this.changeRowId = function(oldRowId,newRowId){
   				  if (oldRowId==newRowId) return;
/*
				  for (var i=0; i<row.childNodes.length; i++)
					  if (row.childNodes[i]._code)
						  this._compileSCL("-",row.childNodes[i]);      */
                  var row = this.rowsAr[oldRowId]
                  row.idd = newRowId;
                  if(this.UserData[oldRowId]){
                     this.UserData[newRowId] = this.UserData[oldRowId]
                     this.UserData[oldRowId] = null;
                  }
	                if (this._h2 && this._h2.get[oldRowId]){
	                	this._h2.get[newRowId]=this._h2.get[oldRowId];
	                	this._h2.get[newRowId].id=newRowId;
	                	delete this._h2.get[oldRowId];
                    }
                  
				  if (this.rowsBuffer[0]){
				  	var ind=this.rowsBuffer[0]._dhx_find(oldRowId);
				  	if (ind!=-1)
				  		this.rowsBuffer[0][ind]==newRowId;
				  }
				  	
                  this.rowsAr[oldRowId] = null;
                  this.rowsAr[newRowId] = row;
				  for (var i=0; i<row.childNodes.length; i++)
					  if (row.childNodes[i]._code)
						  row.childNodes[i]._code=this._compileSCL(row.childNodes[i]._val,row.childNodes[i]);
               }
   /**
   *   @desc: sets ids to every column. Can be used then to retreive the index of the desired colum
   *   @param: [ids] - delimitered list of ids (default delimiter is ","), or empty if to use values set earlier
   *   @type: public
   *   @topic: 3
   */
   this.setColumnIds = function(ids){
                     if(ids)
                        this.columnIds = ids.split(this.delim)
                if (this.hdr.rows.length>0){
                        if(this.hdr.rows[0].cells.length>=this.columnIds.length){
                           for(var i=0;i<this.columnIds.length;i++){
                              this.hdr.rows[0].cells[i].column_id = this.columnIds[i];
                           }
                        }
                }
                  }
   /**
   *   @desc: sets ids to specified column.
   *   @param: ind- index of column
   *   @param: id- id of column
   *   @type: public
   *   @topic: 3
   */
   this.setColumnId = function(ind, id){  this.columnIds[ind]=this.hdr.rows[0].cells[ind].column_id = id; }
   /**
   *   @desc: gets column index by column id
   *   @param: id - column id
   *   @returns: index of the column
   *   @type: public
   *   @topic: 3
   */
   this.getColIndexById = function(id){
                     for(var i=0;i<this.hdr.rows[0].cells.length;i++){
                        if(this.hdr.rows[0].cells[i].column_id==id)
                           return i;
                     }
                  }
   /**
   *   @desc: gets column id of column specified by index
   *   @param: cin - column index
   *   @returns: column id
   *   @type: public
   *   @topic: 3
   */
   this.getColumnId = function(cin){
                     return this.hdr.rows[0].cells[cin].column_id
                  }
	/**
   *   @desc: gets label of column specified by index
   *   @param: cin - column index
   *   @returns: column label
   *   @type: public
   *   @topic: 3
   */
	this.getColumnLabel = function(cin,rin){
		return this.getHeaderCol(cin,rin);
	}
   /**
   *   @desc: gets label of column specified by index
   *   @param: cin - column index
   *   @returns: column label
   *   @type: deprecated
   *	@newmethod: getColumnLabel
   *   @topic: 3
   */
   this.getHeaderCol = function(cin,ind){
   		var z=this.hdr.rows[(ind||0)+1];
   		var n=z.cells[z._childIndexes?z._childIndexes[parseInt(cin)]:cin];
   		return (_isIE?n.innerText:n.textContent);
    }

   /**
   *   @desc: sets row text BOLD
   *   @param: row_id - row id
   *   @type: public
   *   @topic: 2,6
   */
   this.setRowTextBold = function(row_id){
                     this.getRowById(row_id).style.fontWeight = "bold";
                  }
   /**
   *   @desc: sets style to row
   *   @param: row_id - row id
   *   @param: styleString - style string in common format (exmpl: "color:red;border:1px solid gray;")
   *   @type: public
   *   @topic: 2,6
   */
   this.setRowTextStyle = function(row_id,styleString){
                     var r = this.getRowById(row_id)
                     for(var i=0;i<r.childNodes.length;i++){
                                 var pfix="";

//#__pro_feature:21092006{
//#column_hidden:21092006{
                                 if ((this._hrrar)&&(this._hrrar[i]))  pfix="display:none;";
//#}
//#}
                                 if (_isIE)
                                    r.childNodes[i].style.cssText = pfix+"width:"+r.childNodes[i].style.width+";"+styleString;
                                 else
                            r.childNodes[i].style.cssText = pfix+"width:"+r.childNodes[i].style.width+";"+styleString;
                     }

                  }
   /**
   *   @desc: sets background color of row (via bgcolor attribute)
   *   @param: row_id - row id
   *   @param: color - color value
   *   @type: public
   *   @topic: 2,6
   */
   this.setRowColor = function(row_id,color){
		var r = this.getRowById(row_id)
		for(var i=0;i<r.childNodes.length;i++)
			r.childNodes[i].bgColor=color;
	}
   /**
   *   @desc: sets style to cell
   *   @param: row_id - row id
   *   @param: ind - cell index
   *   @param: styleString - style string in common format (exmpl: "color:red;border:1px solid gray;")
   *   @type: public
   *   @topic: 2,6
   */
   this.setCellTextStyle = function(row_id,ind,styleString){
                     var r = this.getRowById(row_id)
                            if (!r) return;
                            var cell=r.childNodes[r._childIndexes?r._childIndexes[ind]:ind];
                            if (!cell) return;
                                 var pfix="";
//#__pro_feature:21092006{
//#column_hidden:21092006{
                                 if ((this._hrrar)&&(this._hrrar[ind]))  pfix="display:none;";
//#}
//#}
                                 if (_isIE)
                                    cell.style.cssText = pfix+"width:"+cell.style.width+";"+styleString;
                                 else
                            cell.style.cssText = pfix+"width:"+cell.style.width+";"+styleString;
                     
                  }

   /**
   *   @desc: sets row text weight to normal
   *   @param: row_id - row id
   *   @type: public
   *   @topic: 2,6
   */
   this.setRowTextNormal = function(row_id){
                     this.getRowById(row_id).style.fontWeight = "normal";
                  }
   /**
   *   @desc: determines if row with specified id exists
   *   @param: row_id - row id
   *   @returns: true if exists, false otherwise
   *   @type: public
   *   @topic: 2,7
   */
   this.doesRowExist = function(row_id){
   	if(this.getRowById(row_id)!=null)
	   return true
	else
	   return false
   	
   }
   
   /**
   *   @desc: determines if row with specified id exists
   *   @param: row_id - row id
   *   @returns: true if exists, false otherwise
   *   @type: deprecated
   *   @topic: 2,7
   */
   this.isItemExists = function(row_id){
                    return this.doesRowExist(row_id) 
                  }

   /**
   *   @desc: gets number of rows in grid
   *   @returns: number of rows in grid
   *   @type: public
   *   @topic: 2,7
   */
   this.getRowsNum = function(){
                     if (this._dload)
                        return  this.limit;
                     return this.rowsCol.length+this.rowsBuffer[0].length;
                  }
   /**
   *   @desc: gets number of columns in grid
   *   @returns: number of columns in grid
   *   @type: public
   *   @topic: 3,7
   */
   this.getColumnsNum = function(){
                     return this.hdr.rows[0].cells.length;
                  }
   /**
   *   @desc: gets number of columns in grid
   *   @returns: number of columns in grid
   *   @type: deprecated
   *   @topic: 3,7
   */
   this.getColumnCount = function(){
                     return this.hdr.rows[0].cells.length;
                  }

   /**
   *   @desc: moves row one position up if possible
   *   @param: row_id -  row id
   *   @type: public
   *   @topic: 2
   */
   this.moveRowUp = function(row_id){
                     var r = this.getRowById(row_id)
                     if (this.isTreeGrid()) return this.moveRowUDTG(row_id,-1);
                     var rInd = this.rowsCol._dhx_find(r)
                                if ((r.previousSibling)&&(rInd!=0)){
        	                        r.parentNode.insertBefore(r,r.previousSibling)
		                            this.rowsCol._dhx_swapItems(rInd,rInd-1)
                                    this.setSizes();
                                    if (this._cssEven)
                                    	this._fixAlterCss(rInd-1);
                                    }
                  }
   /**
   *   @desc: moves row one position down if possible
   *   @param: row_id -  row id
   *   @type: public
   *   @topic: 2
   */
   this.moveRowDown = function(row_id){
                     var r = this.getRowById(row_id)
					 if (this.isTreeGrid()) return this.moveRowUDTG(row_id,1);
					 var rInd = this.rowsCol._dhx_find(r);
					
					 
                            if (r.nextSibling){
	                            this.rowsCol._dhx_swapItems(rInd,rInd+1)							
                                if (r.nextSibling.nextSibling)
                                  r.parentNode.insertBefore(r,r.nextSibling.nextSibling)
                                else
                                    r.parentNode.appendChild(r)
                                this.setSizes();
                                if (this._cssEven)
                                    	this._fixAlterCss(rInd);
                                }
                  }
   /**
   *   @desc: gets dhtmlXGridCellObject object (if no arguments then gets dhtmlXGridCellObject object of currently selected cell)
   *   @param: row_id -  row id
   *   @param: col -  column index
   *   @returns: dhtmlXGridCellObject object (see its methods below)
   *   @type: public
   *   @topic: 4
   */
   this.cellById = function(row_id,col){
   		return this.cells(row_id,col);
   }
   /**
   *   @desc: gets dhtmlXGridCellObject object (if no arguments then gets dhtmlXGridCellObject object of currently selected cell)
   *   @param: row_id -  row id
   *   @param: col -  column index
   *   @returns: dhtmlXGridCellObject object (use it to get/set value to cell etc.)
   *   @type: public
   *   @topic: 4
   */
   this.cells = function(row_id,col){
                     if(arguments.length==0)
                           return this.cells4(this.cell);
                     else
                        var c = this.getRowById(row_id);
                        if (!c && !window.eXcell_math) dhtmlxError.throwError("cell","Row not exists",[row_id,col]);
                        var cell=(c._childIndexes?c.childNodes[c._childIndexes[col]]:c.childNodes[col]);
                  return this.cells4(cell);
                  }
   /**
   *   @desc: gets dhtmlXGridCellObject object
   *   @param: row_index -  row index
   *   @param: col -  column index
   *   @returns: dhtmlXGridCellObject object (see its methods below)
   *   @type: public
   *   @topic: 4
   */
   this.cellByIndex = function(row_index,col){
   		return this.cells2(row_index,col);
   }
   /**
   *   @desc: gets dhtmlXGridCellObject object
   *   @param: row_index -  row index
   *   @param: col -  column index
   *   @returns: dhtmlXGridCellObject object (see its methods below)
   *   @type: public
   *   @topic: 4
   */
   this.cells2 = function(row_index,col){
      var c = this.rowsCol[parseInt(row_index)];
      if (!c && !window.eXcell_math) dhtmlxError.throwError("cell","Row not exists",[row_id,col]);
      var cell=(c._childIndexes?c.childNodes[c._childIndexes[col]]:c.childNodes[col]);
      return this.cells4(cell);
                  }

   /**
   *   @desc: gets exCell editor for row  object and column id
   *   @type: private
   *   @topic: 4
   */
   this.cells3 = function(row,col){
        var cell=(row._childIndexes?row.childNodes[row._childIndexes[col]]:row.childNodes[col]);
      return this.cells4(cell);
                 }
   /**
   *   @desc: gets exCell editor for cell  object
   *   @type: private
   *   @topic: 4
   */
   this.cells4 = function(cell){
   	  var type=window["eXcell_"+(cell._cellType||this.cellType[cell._cellIndex])];
   	  if (type) return new type(cell);
   	  //dhtmlxError.throwError("Incorrect cell type : "+type);
    }
	this.cells5 = function(cell){
		var type=cell._cellType||this.cellType[cell._cellIndex];
		if (!this._ecache[type])
			this._ecache[type]=eval("new eXcell_"+type+"(cell)");
		this._ecache[type].cell=cell;
		return this._ecache[type];
	}    
	this.dma=function(mode){
		if (!this._ecache) this._ecache={};
		if (mode && !this._dma){
			this._dma=this.cells4;
			this.cells4=this.cells5;
		} else if (!mode && this._dma){
			this.cells4=this._dma;
			this._dma=null;
		}
                  }
   /**
   * @desc: gets Combo object of specified column. Use it to change select box value for cell before editor opened
   *   @type: public
   *   @topic: 3,4
   *   @param: col_ind - index of the column to get combo object for
   */
   this.getCombo = function(col_ind){
      if(!this.combos[col_ind]){
         this.combos[col_ind] = new dhtmlXGridComboObject();
      }
      return this.combos[col_ind];
   }
   /**
   *   @desc: sets user data to row
   *   @param: row_id -  row id. if empty then user data is set for grid (not row)
   *   @param: name -  name of user data block
   *   @param: value -  value of user data block
   *   @type: public
   *   @topic: 2,5
   */
   this.setUserData = function(row_id,name,value){
                     try{
                        if(row_id=="")
                           row_id = "gridglobaluserdata";
                        if(!this.UserData[row_id])
                           this.UserData[row_id] = new Hashtable()
                        this.UserData[row_id].put(name,value)
                     }catch(er){
                        alert("UserData Error:"+er.description)
                     }
                  }
   /**
   *   @desc: gets user Data
   *   @param: row_id -  row id. if empty then user data is for grid (not row)
   *   @param: name -  name of user data
   *   @returns: value of user data
   *   @type: public
   *   @topic: 2,5
   */
   this.getUserData = function(row_id,name){
   			this.getRowById(row_id);//parse row if necessary
            if(row_id=="")
               row_id = "gridglobaluserdata";
                var z=this.UserData[row_id];
               return (z?z.get(name):"");
      }

   /**
   *   @desc: manage editibility of the grid
   *   @param: [fl] - set not editable if FALSE, set editable otherwise
   *   @type: public
   *   @topic: 7
   */
   this.setEditable = function(fl){
                     this.isEditable = convertStringToBoolean(fl);
                  }
   /**
   *   @desc: selects row
   *   @param: row_id - row id
   *   @param: multiFL - VOID. select multiple rows
   *   @param: show - true/false - scroll row to view, true by defaul    
   *   @param: call - true to call function on select
   *   @type: deprecated
   *   @topic: 1,2
   */
   this.setSelectedRow = function(row_id, multiFL,show,call){ 
                     if(!call)
                        call = false;
                     this.selectCell(this.getRowById(row_id),0,call,multiFL,false,show);
                  }
   /**
   *   @desc: removes selection from the grid
   *   @type: public
   *   @topic: 1,9
   */
   this.clearSelection = function(){
                     this.editStop()
                     for(var i=0;i<this.selectedRows.length;i++){
                        var r=this.rowsAr[this.selectedRows[i].idd];
                        if (r) r.className=r.className.replace(/rowselected/g,"");
                     }

                     //..
                     this.selectedRows = new dhtmlxArray(0)
                     this.row = null;
                     if(this.cell!=null){
                        this.cell.className = this.cell.className.replace(/cellselected/g,"");
                        this.cell = null;
                     }
                  }
   /**
   *   @desc: copies row content to another existing row
   *   @param: from_row_id - id of the row to copy content from
   *   @param: to_row_id - id of the row to copy content to
   *   @type: public
   *   @topic: 2,5
   */
   this.copyRowContent = function(from_row_id, to_row_id){
                     var frRow = this.getRowById(from_row_id)

                            if (!this.isTreeGrid())
                         for(var i=0;i<frRow.cells.length;i++){
                            this.cells(to_row_id,i).setValue(this.cells(from_row_id,i).getValue())
                         }
                            else
                                this._copyTreeGridRowContent(frRow,from_row_id,to_row_id);

                     //for Mozilla (to avaoid visual glitches)
                     if(!isIE())
                        this.getRowById(from_row_id).cells[0].height = frRow.cells[0].offsetHeight
                  }



	/**
   *   @desc: sets new column header label
   *   @param: col - header column index
   *   @param: label - new label for the cpecified header's column. Can contai img:[imageUrl]Text Label
   *	@param: ind - header row index (default is 0)
   *   @type: public
   *   @topic: 3,6
   */
	this.setColumnLabel = function(c,label,ind){
		this.setHeaderCol(c,label,ind);
	}
   /**
   *   @desc: sets new column header label
   *   @param: col - header column index
   *   @param: label - new label for the cpecified header's column. Can contai img:[imageUrl]Text Label
   *	@param: ind - header row index (default is 0)
   *   @type: public
   *   @topic: 3,6
   */
   this.setHeaderCol = function(c,label,ind){
                     var z=this.hdr.rows[ind||1];
                var col=(z._childIndexes?z._childIndexes[c]:c);
                     if(!this.useImagesInHeader){
                        var hdrHTML = "<div class='hdrcell'>"
                  if(label.indexOf('img:[')!=-1){
                     var imUrl = label.replace(/.*\[([^>]+)\].*/,"$1");
                     label = label.substr(label.indexOf("]")+1,label.length)
                     hdrHTML+="<img width='18px' height='18px' align='absmiddle' src='"+imUrl+"' hspace='2'>"
                  }
                  hdrHTML+=label;
                  hdrHTML+="</div>";
                  z.cells[col].innerHTML = hdrHTML;
                  if (this._hstyles[col]) z.cells[col].style.cssText = this._hstyles[col];

                }else{//if images in header header
                        z.cells[col].style.textAlign = "left";
                        z.cells[col].innerHTML = "<img src='"+this.imgURL+""+label+"' onerror='this.src = \""+this.imgURL+"imageloaderror.gif\"'>";
                        //preload sorting headers (asc/desc)
                        var a = new Image();
                        a.src = this.imgURL+""+label.replace(/(\.[a-z]+)/,".desc$1");
                        this.preloadImagesAr[this.preloadImagesAr.length] = a;
                        var b = new Image();
                        b.src = this.imgURL+""+label.replace(/(\.[a-z]+)/,".asc$1");
                        this.preloadImagesAr[this.preloadImagesAr.length] = b;
                     }
                     
	if ((label||"").indexOf("#")!=-1){
  		var t=label.match(/(^|{)#([^}]+)(}|$)/);
  		if (t){
  			var tn="_in_header_"+t[2];
  			if (this[tn]) this[tn]((this.forceDivInHeader?z.cells[col].firstChild:z.cells[col]),col,label.split(t[0]));
  		}
  	}                     
                  }
   /**
   *   @desc: deletes all rows in grid
   *   @param: header - (boolean) enable/disable cleaning header
   *   @type: public
   *   @topic: 5,7,9
   */
   this.clearAll = function(header){
		if (this._h2){
			this._h2=new dhtmlxHierarchy();
			if (this._fake){
				if (this._realfake)
		  				this._h2=this._fake._h2;
		  			else
		  				this._fake._h2=this._h2;
		 	}
		 }

                  this.limit=this._limitC=0;
                            this.editStop();
                        if (this._dLoadTimer)  window.clearTimeout(this._dLoadTimer);
                            if (this._dload){
                               this.objBox.scrollTop=0;
                               this.limit=this._limitC||0;
                               this._initDrF=true;
                               }

                     var len = this.rowsCol.length;
                     //treegrid
                     if(this.loadedKidsHash!=null){
                        this.loadedKidsHash.clear();
                                this.loadedKidsHash.put("hashOfParents",new Hashtable());
                     }
                     //for some case
                     len = this.obj._rowslength();

                     for(var i=len-1;i>=0;i--){
                       var t_r=this.obj._rows(i);
                        t_r.parentNode.removeChild(t_r);
                     }
                if (header && this.obj.rows[0]){
                    this.obj.rows[0].parentNode.removeChild(this.obj.rows[0]);
                        for(var i=this.hdr.rows.length-1;i>=0;i--){
                          var t_r=this.hdr.rows[i];
                           t_r.parentNode.removeChild(t_r);
                        }
                        if (this.ftr){
                        	this.ftr.parentNode.removeChild(this.ftr);
                        	this.ftr=null;
                        }               
               		this._aHead=this.ftr=this._aFoot=null;
               		this._hrrar=[];
                }

                     //..
                     this.row = null;
                     this.cell = null;


                     this.rowsCol = new dhtmlxArray(0)
                     this.rowsAr = new Array(0);//array of rows by idd
                     this.rowsBuffer = new Array(new dhtmlxArray(0),new dhtmlxArray(0));//buffer of rows loaded, but not rendered (array of ids, array of cell values arrays)
                     this.UserData = new Array(0)
					 this.selectedRows = new dhtmlxArray(0);

                     if(this.pagingOn){
                     	this.xmlFileUrl="";
                     	this.recordsNoMore=null;
                        this.changePage(1);
                        //this.createPagingBlock();
                     }

             //  if (!this._fake){
               	/*
                   if ((this._hideShowColumn)&&(this.hdr.rows[0]))
                      for (var i=0; i<this.hdr.rows[0].cells.length; i++)
                          this._hideShowColumn(i,"");
               this._hrrar=new Array();*/
            //}
            if (this._contextCallTimer) window.clearTimeout(this._contextCallTimer);


            if (this._sst)
               this.enableStableSorting(true);

               this.setSortImgState(false); 
                    this.setSizes();
                    //this.obj.scrollTop = 0;
            
            this.callEvent("onClearAll",[]);
   }


   /**
   *   @desc: sorts grid by specified field
   *    @invoke: header click
   *   @param: [ind] - index of the field
   *   @param: [repeatFl] - if to repeat last sorting
   *   @type: private
   *   @topic: 3
   */
   this.sortField = function(ind,repeatFl,r_el){
                  if(this.getRowsNum()==0)
                     return false;
                  var el = this.hdr.rows[0].cells[ind];
                        if (!el) return; //somehow
             // if (this._dload  && !this.callEvent("onBeforeSorting",[ind,this]) ) return true;

                  if(el.tagName == "TH" && (this.fldSort.length-1)>=el._cellIndex && this.fldSort[el._cellIndex]!='na'){//this.entBox.fieldstosort!="" &&
                     if((((this.sortImg.src.indexOf("_desc.gif")==-1) && (!repeatFl)) || ((this.sortImg.style.filter!="") && (repeatFl))) && (this.fldSorted==el))
                        var sortType = "des";
                     else
                        var sortType = "asc";

				  if (!this.callEvent("onBeforeSorting",[ind,this,sortType])) return;
				  this.sortImg.src = this.imgURL+"sort_"+(sortType=="asc"?"asc":"desc")+".gif";

                     //for header images
                     if(this.useImagesInHeader){
                   var cel=this.hdr.rows[1].cells[el._cellIndex].firstChild;
                        if(this.fldSorted!=null){
                     var celT=this.hdr.rows[1].cells[this.fldSorted._cellIndex].firstChild;
                           celT.src = celT.src.replace(/\.[ascde]+\./,".");
                        }
                        cel.src = cel.src.replace(/(\.[a-z]+)/,"."+sortType+"$1")
                     }
                     //.
                     this.sortRows(el._cellIndex,this.fldSort[el._cellIndex],sortType)
                     this.fldSorted = el;this.r_fldSorted = r_el;
                var c=this.hdr.rows[1];
                var c=r_el.parentNode;
                     var real_el=c._childIndexes?c._childIndexes[el._cellIndex]:el._cellIndex;
                     this.setSortImgPos(false,false,false,r_el);
                     this.callEvent("onAfterSorting",[]);
                  }
               }

//#__pro_feature:21092006{
//#custom_sort:21092006{
    /**
    *   @desc: set custom sorting (custom sort has three params - valueA,valueB,order; where order can be asc or des)
    *   @param: func - function to use for comparison
    *   @param:   col - index of column to apply custom sorting to
    *   @type: public
    *   @edition: Professional
    *   @topic: 3
    */
    this.setCustomSorting = function(func,col){
       if (!this._customSorts) this._customSorts=new Array();
       this._customSorts[col] = (typeof(func)=="string")?eval(func):func;
       this.fldSort[col]="cus";
    }
//#}
//#}

   /**
   *   @desc: specify if values passed to Header are images file names
   *   @param: fl - true to treat column header values as image names
   *   @type: public
   *   @before_init: 1
   *   @topic: 0,3
   */
   this.enableHeaderImages = function(fl){
      this.useImagesInHeader = fl;
   }

   /**
   *   @desc: set header label and default params for new headers
   *   @param: hdrStr - header string with delimiters
   *   @param: splitSign - string used as a split marker, optional. Default is "#cspan"
   *   @param: styles - array of header styles
   *   @type: public
   *   @before_init: 1
   *   @topic: 0,3
   */
   this.setHeader = function(hdrStr,splitSign,styles){
   	if (typeof(hdrStr)!="object")
      var arLab = this._eSplit(hdrStr);
    else arLab=[].concat(hdrStr);
    
      var arWdth = new Array(0);
      var arTyp = new dhtmlxArray(0);
      var arAlg = new Array(0);
      var arVAlg = new Array(0);
      var arSrt = new Array(0);
      for(var i=0;i<arLab.length;i++){
         arWdth[arWdth.length] = Math.round(100/arLab.length);
         arTyp[arTyp.length] = "ed";
         arAlg[arAlg.length] = "left";
         arVAlg[arVAlg.length] = "";//top
         arSrt[arSrt.length] = "na";
      }

      this.splitSign = splitSign||"#cspan";
      this.hdrLabels = arLab;
      this.cellWidth = arWdth;
      this.cellType =  arTyp;
      this.cellAlign =  arAlg;
      this.cellVAlign =  arVAlg;
      this.fldSort = arSrt;
      this._hstyles = styles||[];
   }
   	/**
   *   @desc: 
   *   @param: str - ...
   *   @type: private
   */
	this._eSplit=function(str){
		if (![].push) return str.split(this.delim);
	 	var a="r"+(new Date()).valueOf();
	 	var z=this.delim.replace(/([\|\+\*\^])/g,"\\$1")
   		return (str||"").replace(RegExp(z,"g"),a).replace(RegExp("\\\\"+a,"g"),this.delim).split(a); 
   		
	}

   /**
   *   @desc: get column type by column index
   *   @param: cInd - column index
   *   @returns:  type code
   *   @type: public
   *   @topic: 0,3,4
   */
    this.getColType = function(cInd) {
       return this.cellType[cInd];
    }

   /**
   *   @desc: get column type by column ID
   *   @param: cID - column id
   *   @returns:  type code
   *   @type: public
   *   @topic: 0,3,4
   */
    this.getColTypeById = function(cID) {
       return this.cellType[this.getColIndexById(cID)];
    }

   /**
   *   @desc: set column types
   *   @param: typeStr - type codes list (default delimiter is ",")
   *   @before_init: 2
   *   @type: public
   *   @topic: 0,3,4
   */
   this.setColTypes = function(typeStr){
      this.cellType = dhtmlxArray(typeStr.split(this.delim));
          this._strangeParams=new Array();
        for (var i=0; i<this.cellType.length; i++)
        if ((this.cellType[i].indexOf("[")!=-1))
            {
                var z=this.cellType[i].split(/[\[\]]+/g);
                this.cellType[i]=z[0];
                this.defVal[i]=z[1];
                if (z[1].indexOf("=")==0){
                    this.cellType[i]="math";
                    this._strangeParams[i]=z[0];
                    }
            }
   }
   /**
   *   @desc: set column sort types (avaialble: str, int, date, na or function object for custom sorting)
   *   @param: sortStr - sort codes list with default delimiter
   *   @before_init: 1
   *   @type: public
   *   @topic: 0,3,4
   */
   this.setColSorting = function(sortStr){
      this.fldSort = sortStr.split(this.delim)
//#__pro_feature:21092006{
//#custom_sort:21092006{
        for (var i=0; i<this.fldSort.length; i++)
            if (((this.fldSort[i]).length>4)&&(typeof(window[this.fldSort[i]])=="function"))
                {
                   if (!this._customSorts) this._customSorts=new Array();
                   this._customSorts[i]=window[this.fldSort[i]];
                   this.fldSort[i]="cus";
                }
//#}
//#}
   }
   /**
   *   @desc: set align of values in columns
   *   @param: alStr - list of align values (possible values are: right,left,center,justify). Default delimiter is ","
   *   @before_init: 1
   *   @type: public
   *   @topic: 0,3
   */
   this.setColAlign = function(alStr){
      this.cellAlign = alStr.split(this.delim)
   }
   /**
   *   @desc: set vertical align of columns
   *   @param: valStr - vertical align values list for columns (possible values are: baseline,sub,super,top,text-top,middle,bottom,text-bottom)
   *   @before_init: 1
   *   @type: public
   *   @topic: 0,3
   */
   this.setColVAlign = function(valStr){
      this.cellVAlign = valStr.split(this.delim)
   }

   /**
   *   @desc: sets grid to multiline row support (call before init)
   *   @param:   fl - true to set multiline support
   *   @type: deprecated
   *   @before_init: 1
   *   @topic: 0,2
   */
   this.setMultiLine = function(fl){
      if(fl==true)
         this.multiLine = -1;
   }
   /**
   * 	@desc: create grid with no header. Call before initialization, but after setHeader. setHeader have to be called in any way as it defines number of columns
   *   @param: fl - true to use no header in the grid
   *   @type: public
   *   @before_init: 1
   *   @topic: 0,7
   */
   this.setNoHeader = function(fl){
      if(convertStringToBoolean(fl)==true)
         this.noHeader = true;
   }
   /**
   *   @desc: scrolls row to the visible area
   *   @param: rowID - row id
   *   @type: public
   *   @topic: 2,7
   */
   this.showRow = function(rowID){
      if(this.pagingOn){
         if (this.rowsAr[rowID])
            this.changePage(Math.floor(this.getRowIndex(rowID)/this.rowsBufferOutSize)+1);
         else
            while((!this.rowsAr[rowID]) && ( this.rowsBuffer[0].length>0 || !this.recordsNoMore ))
               this.changePage(this.currentPage+1);
      }
	  var c=this.getRowById(rowID).cells[0]; while (c && c.style.display=="none") c=c.nextSibling;
      if (c) this.moveToVisible(c,true)
   }

   /**
   *   @desc: modify default style of grid and its elements. Call before or after Init
   *   @param: ss_header - style def. expression for header
   *   @param: ss_grid - style def. expression for grid cells
   *   @param: ss_selCell - style def. expression for selected cell
   *   @param: ss_selRow - style def. expression for selected Row
   *   @type: public
   *   @before_init: 2
   *   @topic: 0,6
   */
   this.setStyle = function(ss_header,ss_grid,ss_selCell,ss_selRow){
      this.ssModifier = [ss_header, ss_grid , ss_selCell,ss_selCell, ss_selRow];
     var prefs=["#"+this.entBox.id+" table.hdr td","#"+this.entBox.id+" table.obj td","#"+this.entBox.id+" table.obj tr.rowselected td.cellselected","#"+this.entBox.id+" table.obj td.cellselected","#"+this.entBox.id+" table.obj tr.rowselected td"];

     for (var i=0; i<prefs.length; i++)
      if (this.ssModifier[i]){
         if (_isIE)
            this.styleSheet[0].addRule(prefs[i],this.ssModifier[i]);
             else
            this.styleSheet[0].insertRule(prefs[i]+" { "+this.ssModifier[i]+" } ",0);
      }
   }
   /**
   *   @desc: colorize columns  background.
   *   @param: clr - colors list
   *   @type: public
   *   @before_init: 1
   *   @topic: 3,6
   */
   this.setColumnColor = function(clr){
      this.columnColor = clr.split(this.delim)
   }

   /**
   *   @desc: set even/odd css styles
   *   @param: cssE - name of css class for even rows
   *   @param: cssU - name of css class for odd rows
   *   @param: perLevel - true/false - mark rows not by order, but by level in treegrid
   *   @param: levelUnique - true/false - creates additional unique css class based on row level
   *   @type: public
   *   @before_init: 1
   *   @topic: 3,6
   */
   this.enableAlterCss = function(cssE,cssU,perLevel,levelUnique){
        if (cssE||cssU)
            this.setOnGridReconstructedHandler(function(){ 
            	if (!this._cssSP)
                	this._fixAlterCss();
            });


	  this._cssSP=perLevel;
	  this._cssSU=levelUnique;
	  this._cssEven = cssE;
      this._cssUnEven = cssU;
   }

   /**
   *   @desc: recolor grid from defined point
   *   @type: private
   *   @before_init: 1
   *   @topic: 3,6
   */
   this._fixAlterCss = function(ind){
 		if (this._cssSP && this.isTreeGrid()) return this._fixAlterCssTG(ind);
        ind=ind||0;
        var j=ind;
        for (var i=ind; i<this.rowsCol.length; i++){
            if (!this.rowsCol[i]) continue;
            if (this.rowsCol[i].style.display!="none"){
            if (this.rowsCol[i].className.indexOf("rowselected")!=-1){
                if (j%2==1)
                    this.rowsCol[i].className=this._cssUnEven+" rowselected"+(this.rowsCol[i]._css||"");
                else
                    this.rowsCol[i].className=this._cssEven+" rowselected"+(this.rowsCol[i]._css||"");
            }
            else{
                if (j%2==1)
                    this.rowsCol[i].className=this._cssUnEven+(this.rowsCol[i]._css||"");
                else
                    this.rowsCol[i].className=this._cssEven+(this.rowsCol[i]._css||"");
            }
                j++;
            }
        }
   }

//#__pro_feature:21092006{
/**
*     @desc: clear wasChanged state for all cells in grid
*     @type: public
*     @edition: Professional
*     @topic: 7
*/
this.clearChangedState = function(){
   for (var i=0; i<this.rowsCol.length; i++){
      var row=this.rowsCol[i];
      var cols=row.childNodes.length;
      for (var j=0; j<cols; j++)
         row.childNodes[j].wasChanged=false;
   }
};

/**
*     @desc: get list of IDs of changed rows
*     @type: public
*     @edition: Professional
*     @return: list of ID of changed rows
*     @topic: 7
*/
this.getChangedRows = function(){
   var res=new Array();
   this.forEachRow(function(id){
      var row=this.rowsAr[id];
      var cols=row.childNodes.length;
      for (var j=0; j<cols; j++)
        if (row.childNodes[j].wasChanged) {
         res[res.length]=row.idd;
         break;
         }
	   })
   return res.join(this.delim);
};


//#serialization:21092006{

this._sUDa = false;
this._sAll = false;

/**
*     @desc: configure XML serialization
*     @type: public
*     @edition: Professional
*     @param: userData - enable/disable user data serialization
*     @param: fullXML - enable/disable full XML serialization (selection state)
*     @param: config - serialize grid configuration
*     @param: changedAttr - include changed attribute
*     @param: onlyChanged - include only Changed  rows in result XML
*     @param: asCDATA - output cell values as CDATA sections (prevent invalid XML)
*     @topic: 0,5,7
*/
this.setSerializationLevel = function(userData,fullXML,config,changedAttr,onlyChanged,asCDATA){
   this._sUDa = userData;
   this._sAll = fullXML;
   this._sConfig = config;
   this._chAttr = changedAttr;
   this._onlChAttr = onlyChanged;
   this._asCDATA = asCDATA;
}



/**
*     @desc: configure which column must be serialized (if you do not use this method, then all columns will be serialized)
*     @type: public
*     @edition: Professional
*     @param: list - list of true/false values separated by comma, if list empty then all fields will be serialized
*     @topic: 0,5,7
*/
this.setSerializableColumns=function(list){
    if (!list) {
        this._srClmn=null;
        return;
        }
    this._srClmn=(list||"").split(",");
    for (var i=0; i<this._srClmn.length; i++)
        this._srClmn[i]=convertStringToBoolean(this._srClmn[i]);
}

/**
*     @desc: serialize a collection of rows
*     @type: private
*     @topic: 0,5,7
*/
this._serialise = function(rCol,inner,closed){
     this.editStop()
    var out=[];
    //rows collection
    var i=0;
    var j=0;
    var leni=(this._dload)?this.rowsBuffer[0].length:rCol.length;

	if (this.isTreeGrid()){
		var f=function(id,f){
			var str=[];
			var z=self._h2.get[id];
			if (0!=id)
				str.push(self._serializeRow(self.rowsAr[id],i));
			if (z.childs.length==0 && self.rowsAr[id]._xml){
			  var xar=self.rowsAr[id]._xml;
			  for(var i=0; i<xar.length; i++)
				if (self.xmlSerializer)
                   	str.push(self.xmlSerializer.serializeToString(xar[i]));
               	else
                   str.push(xar[i].xml);
			} else
			for(var i=0; i<z.childs.length; i++)
				str.push(f(z.childs[i].id,f));
			if (0!=id)				
				str.push("</row>\n");
			return str.join("");
		}
		out.push(f(0,f));
	}else
    for(i; i<leni; i++){
		var r = rCol[i];
		var temp=this._serializeRow(r,i);
		out.push(temp);
        if ((temp!="") && r && (!r._sRow) && (!r._rLoad))
			out.push("</row>");
   }

    return [out.join(""),j+i];
}

/**
*   @desc: serialize xml node to XML string
*   @param: r - TR or xml node (row)
*   @retruns: string - xml representation of passed row
*   @type: private
*/
this._manualXMLSerialize = function(r){
   var out = "<row id='"+r.getAttribute("id")+"'>";
   var i=0;
    for(var jj=0;jj<r.childNodes.length;jj++){
      var z=r.childNodes[jj];
      if (z.tagName!="cell") continue;
        if ((!this._srClmn)||(this._srClmn[i]))
         out += "<cell>"+(z.firstChild?z.firstChild.data:"")+"</cell>";
      i++;
      }
   out+="</row>";
    return out;
}


/**
*   @desc: serialize TR or xml node to grid formated xml (row tag)
*   @param: r - TR or xml node (row)
*   @retruns: string - xml representation of passed row
*   @type: private
*/
this._serializeRow = function(r,i){
    var out = [];
    if ((!r)||(r._sRow)||(r._rLoad)) {
		if (this._onlChAttr) return "";
         if (this.rowsBuffer[1][i]){
               if (this.xmlSerializer)
                   out=this.xmlSerializer.serializeToString(this.rowsBuffer[1][i]);
               else
                   out=this.rowsBuffer[1][i].xml;
         }
         return out;
     }


      var selStr = "";

      //serialize selection
      if(this._sAll && this.selectedRows._dhx_find(r)!=-1)
         selStr = " selected='1'";
      out.push("<row id='"+r.idd+"'"+selStr+" "+((this._h2 && this._h2.get[r.idd].state=="minus")?"open='1'":"")+">");
      //userdata
      if(this._sUDa && this.UserData[r.idd]){
         keysAr = this.UserData[r.idd].getKeys()
           for(var ii=0;ii<keysAr.length;ii++){
            out.push("<userdata name='"+keysAr[ii]+"'>"+this.UserData[r.idd].get(keysAr[ii])+"</userdata>");
         }
      }


      //cells
     var changeFl=false;
      for(var jj=0;jj<r.childNodes.length;jj++){
            if ((!this._srClmn)||(this._srClmn[jj]))
                {
                var cvx=r.childNodes[jj];
                out.push("<cell");

                var zx=this.cells(r.idd,cvx._cellIndex);
                if (zx.cell)
                    zxVal=zx[this._agetm]();
                else zxVal="";

            if (zxVal===null) zxVal="";
            if (this._asCDATA)
               zxVal="<![CDATA["+zxVal+"]]>";

//#colspan:20092006{
                if ((this._ecspn)&&(cvx.colSpan)&&cvx.colSpan>1)
                    out.push(" colspan=\""+cvx.colSpan+"\" ");
//#}

			if( zx.getSerializeAttributes )
     			out.push(" "+zx.getSerializeAttributes());


            if (this._chAttr){
               if (zx.wasChanged()){
                  out.push(" changed=\"1\"");
                  changeFl=true;
                  }
               }
            else
               if ((this._onlChAttr)&&(zx.wasChanged())) changeFl=true;

                if (this._sAll)
                  out.push((this._h2?(" image='"+this._h2.get[r.idd].image+"'"):"")+">"+zxVal+"</cell>");
                else
                 out.push(">"+zxVal+"</cell>");
//#colspan:20092006{
                if ((this._ecspn)&&(cvx.colSpan)){
                    cvx=cvx.colSpan-1;
                    for (var u=0; u<cvx; u++)
                        out.push("<cell/>");
                        }
//#}
                }
      }
     if ((this._onlChAttr)&&(!changeFl)&&(!r._added)) return "";
      return out.join("");
}

/**
*     @desc: serialize grid configuration
*     @type: private
*     @topic: 0,5,7
*/
this._serialiseConfig=function(){
    var out="<head>";
        for (var i=0; i<this.hdr.rows[0].cells.length; i++){
            out+="<column width='"+this.cellWidthPX[i]+"' align='"+this.cellAlign[i]+"' type='"+this.cellType[i]+"' sort='"+this.fldSort[i]+"' color='"+this.columnColor[i]+"'"+(this.columnIds[i]?(" id='"+this.columnIds[i]+"'"):"")+">";
            out+=this.getHeaderCol(i);
            var z=this.getCombo(i);
            if (z)
                for (var j=0; j<z.keys.length; j++)
                    out+="<option value='"+z.keys[j]+"'>"+z.values[j]+"</option>";
            out+="</column>"
            }
    return out+="</head>";
}
/**
*     @desc: get actual xml of grid. The depth of serialization can be set with setSerializationLevel method
*     @type: public
*     @edition: Professional
*     @topic: 5,7
*/
this.serialize = function(){
    if(_isFF)
      this.xmlSerializer = new XMLSerializer();

   var out='<?xml version="1.0"?><rows>';
        if (this._mathSerialization)
             this._agetm="getMathValue";
        else this._agetm="getValue";

   if(this._sUDa && this.UserData["gridglobaluserdata"]){
      var keysAr = this.UserData["gridglobaluserdata"].getKeys()
      for(var i=0;i<keysAr.length;i++){
         out += "<userdata name='"+keysAr[i]+"'>"+this.UserData["gridglobaluserdata"].get(keysAr[i])+"</userdata>";
      }

   }

    if (this._sConfig)
        out+=this._serialiseConfig();
    out+=this._serialise(this.rowsCol)[0];


    if (!this._dload){
       //rows buffer
       for(var i=0;i<this.rowsBuffer[1].length;i++){
          if(this.rowsBuffer[1][i].tagName=="TR"){

         }else{
         if (!this._onlChAttr){
            if (this._srClmn)
               out += this._manualXMLSerialize(this.rowsBuffer[1][i]);
            else
                  if(!this.xmlSerializer)//ie
                      out += this.rowsBuffer[1][i].xml;
                   else{//mozilla
                      out += this.xmlSerializer.serializeToString(this.rowsBuffer[1][i]);
                   }
         }
         }
       }
    }
   out+='</rows>';
   return out;
}
//#}
//#}

/*SET EVENT HANDLERS*/
//#events_basic:21092006{
   /**
   *     @desc: set function called when row selected  ( event is async )
   *     @param: func - event handling function (or its name)
   *     @param: anyClick - call handler on any click event, react only on changed row by default
   *     @type: deprecated
   *     @topic: 10
   *     @event: onRowSelect
   *     @eventdesc: Event raised immideatly after row was clicked.
   *     @eventparam:  ID of clicked row
   *     @eventparam:  index of clicked cell
   */
   this.setOnRowSelectHandler = function(func,anyClick){
        this.attachEvent("onRowSelect",func);
      this._chRRS=(!convertStringToBoolean(anyClick));
   }


   /**
   *     @desc: set function called on grid scrolling
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *     @event: onScroll
   *     @eventdesc: Event raised immideatly after scrolling occured
   *     @eventparam:  scroll left
   *     @eventparam:  scroll top
   */
   this.setOnScrollHandler = function(func){
        this.attachEvent("onScroll",func);
   }

   /**
   *     @desc: set function called when cell editted
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *   @event: onEditCell
   *     @eventdesc: Event raises 1-3 times depending on cell type and settings
   *     @eventparam:  stage of editting (0-before start[can be canceled if returns false],1-editor opened,2-editor closed)
   *     @eventparam:  ID or row
   *     @eventparam:  index of cell
   *     @eventparam:  new value ( only for stage 2 )
   *     @eventparam:  old value ( only for stage 2 )
   *     @returns:   for stage (0) - false - deny editing; for stag (2) - false - revert to old value, (string) - set (string) instead of new value
   */
   this.setOnEditCellHandler = function(func){
        this.attachEvent("onEditCell",func);
   }
   /**
   *     @desc: set function called when checkbox or radiobutton was clicked
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *     @event: onCheckbox
   *     @eventdesc: Event raises after state was changed.
   *     @eventparam:  ID or row
   *     @eventparam:  index of cell
   *     @eventparam:  state of checkbox/radiobutton
   */
   this.setOnCheckHandler = function(func){
        this.attachEvent("onCheckbox",func);
   }

   /**
   *     @desc: set function called when user press Enter
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *   @event: onEnter
   *     @eventdesc: Event raised immideatly after Enter pressed.
   *     @eventparam:  ID or row
   *     @eventparam:  index of cell
   */
   this.setOnEnterPressedHandler = function(func){
        this.attachEvent("onEnter",func);
   }

   /**
   *     @desc: set function called before row removed from grid
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *      @event: onBeforeRowDeleted
   *     @eventdesc: Event raised right before row deleted (if returns false, deletion canceled)
   *     @eventparam:  ID or row
   */
   this.setOnBeforeRowDeletedHandler = function(func){
        this.attachEvent("onBeforeRowDeleted",func);
   }
   /**
   *     @desc: set function called after row added to grid
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *      @event: onRowAdded
   *     @eventdesc: Event raised right after row was added to grid
   *     @eventparam:  ID or row
   */
   this.setOnRowAddedHandler = function(func){
        this.attachEvent("onRowAdded",func);
   }

   /**
   *     @desc: set function called when row added/deleted or grid reordered
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *     @event: onGridReconstructed
   *     @eventdesc: Event raised immideatly after row was clicked.
   *     @eventparam:  grid object
   */
   this.setOnGridReconstructedHandler = function(func){
        this.attachEvent("onGridReconstructed",func);
   }
/**
*     @desc: set function called on each resizing itteration
*     @param: func - event handling function
*     @type: deprecated

*     @topic: 10
*     @event:  onResize
*     @eventdesc: event fired on each resize itteration
*     @eventparam: cell index
*     @eventparam: cell width
*     @eventparam: grid object
*     @eventreturns: if event returns false - the resizig denied
*/
	dhtmlXGridObject.prototype.setOnResize=function(func){
                this.attachEvent("onResize",func);
    };
       
//#}

//#__pro_feature:21092006{
//#events_adv:21092006{
/**
*     @desc: set function called moment before row selected in grid
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event:  onBeforeSelect
*     @eventdesc: event fired moment before row in grid get selection
*     @eventparam: new selected row
*     @eventparam: old selected row
*     @eventreturns: false - block selection
*/
   dhtmlXGridObject.prototype.setOnBeforeSelect=function(func){
                this.attachEvent("onBeforeSelect",func);
    };
/**
*     @desc: set function called after row created
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event:  onRowCreated
*     @eventdesc: event fired after row created in grid, and filled with data
*     @eventparam: row id
*     @eventparam: row object
*     @eventparam: related xml ( if available )
*/
   dhtmlXGridObject.prototype.setOnRowCreated=function(func){
                this.attachEvent("onRowCreated",func);
    };

/**
*     @desc: set function called after xml loading/parsing ended
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event:  onXLE
*     @eventdesc: event fired simultaneously with ending XML parsing, new items already available in tree
*     @eventparam: grid object
*     @eventparam: count of nodes added
*/
   dhtmlXGridObject.prototype.setOnLoadingEnd=function(func){
                this.attachEvent("onXLE",func);
    };

/**
*     @desc: set function called after value of cell changed by user actions
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event:  onCellChanged
*     @eventdesc: event fired after value was changed
*     @eventparam: row ID
*     @eventparam: cell index
*     @eventparam: new value
*/
   dhtmlXGridObject.prototype.setOnCellChanged=function(func){
                this.attachEvent("onCellChanged",func);
		    }; 
/**
*     @desc: set function called before xml loading started
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event: onXLS
*     @eventdesc: event fired before request for new XML sent to server
*     @eventparam: grid object
*/
   dhtmlXGridObject.prototype.setOnLoadingStart=function(func){
                this.attachEvent("onXLS",func);
    };




/**
*     @desc: set function called before sorting of data started, didn't occur while calling grid.sortRows
*     @param: func - event handling function
*     @type: deprecated
*     @edition: Professional
*     @topic: 10
*     @event:  onBeforeSorting
*     @eventdesc: event called before sorting of data started
*     @eventparam: index of sorted column
*     @eventparam: grid object
*     @eventparam: direction of sorting asc/desc
*     @eventreturns: if event returns false - the sorting denied
*/
   dhtmlXGridObject.prototype.setOnColumnSort=function(func){
            this.attachEvent("onBeforeSorting",func);
        };

   /**
   *     @desc: set function called when row selection changed
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *      @edition: Professional
   *     @event: onSelectStateChanged
   *     @eventdesc: Event raised immideatly after selection state was changed
   *     @eventparam:  ID or list of IDs of selected row(s)
   */
   this.setOnSelectStateChanged = function(func){
        this.attachEvent("onSelectStateChanged",func);
   }

   /**
   *     @desc: set function called when row was dbl clicked
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *      @edition: Professional
   *      @event: onRowDblClicked
   *     @eventdesc: Event raised right after row was double clicked, before cell editor opened by dbl click. If retuns false, event canceled;
   *     @eventparam:  ID or row
   *     @eventparam:  index of column
   */
   this.setOnRowDblClickedHandler = function(func){
        this.attachEvent("onRowDblClicked",func);
   }

   /**
   *     @desc: set function called when header was clicked
   *     @param: func - event handling function (or its name)
   *     @type: deprecated
   *     @topic: 10
   *     @edition: Professional
   *     @event: onHeaderClick
   *     @eventdesc: Event raised right after header was clicked, before sorting or any other actions;
   *     @eventparam:  index of column
   *     @eventparam:  related javascript event object   
   *     @eventreturns: if event returns false - defaul action denied
   */
   this.setOnHeaderClickHandler = function(func){
        this.attachEvent("onHeaderClick",func);
   }



//#}
//#}


/**
*     @desc: set function called after resizing finished
*     @param: func - event handling function
*     @type: deprecated
*     @topic: 10
*     @event:  onResizeEnd
*     @eventdesc: event fired after resizing of column finished
*     @eventparam: grid object
*/
   dhtmlXGridObject.prototype.setOnResizeEnd=function(func){
                this.attachEvent("onResizeEnd",func);
    };

   /**
   *    @desc: returns absolute left and top position of specified element
   *    @returns: array of two values: absolute Left and absolute Top positions
   *    @param: oNode - element to get position of
   *   @type: private
   *   @topic: 8
   */
   this.getPosition = function(oNode,pNode){

                  if(!pNode)
                        var pNode = document.body

                  var oCurrentNode=oNode;
                  var iLeft=0;
                  var iTop=0;
                  while ((oCurrentNode)&&(oCurrentNode!=pNode)){//.tagName!="BODY"){
               iLeft+=oCurrentNode.offsetLeft-oCurrentNode.scrollLeft;
               iTop+=oCurrentNode.offsetTop-oCurrentNode.scrollTop;
               oCurrentNode=oCurrentNode.offsetParent;//isIE()?:oCurrentNode.parentNode;
                  }
              if (pNode == document.body ){
                 if (_isIE){
                 if (document.documentElement.scrollTop)
                  iTop+=document.documentElement.scrollTop;
                 if (document.documentElement.scrollLeft)
                  iLeft+=document.documentElement.scrollLeft;
                  }
                  else
                       if (!_isFF){
                             iLeft+=document.body.offsetLeft;
                           iTop+=document.body.offsetTop;
                  }
                 }
                     return new Array(iLeft,iTop);
               }
   /**
   *   @desc: gets nearest parent of specified type
   *   @param: obj - input object
   *   @param: tag - string. tag to find as parent
   *   @returns: object. nearest paraent object (including spec. obj) of specified type.
   *   @type: private
   *   @topic: 8
   */
   this.getFirstParentOfType = function(obj,tag){
      while(obj && obj.tagName!=tag && obj.tagName!="BODY"){
         obj = obj.parentNode;
      }
      return obj;
   }

/*METHODS deprecated*/
   /**
   *   @desc: deprecated. sets number of columns
   *   @param: cnt - number of columns
   *   @type: void
   *   @topic: 3,7
   */
   this.setColumnCount = function(cnt){alert('setColumnCount method deprecated')}
   /**
   *   @desc: deprecated. repaint of the grid
   *   @topic: 7
   *   @type: void
   */
   this.showContent = function(){alert('showContent method deprecated')}

/*INTERNAL EVENT HANDLERS*/
      this.objBox.onscroll = new Function("","this.grid._doOnScroll()")
    if ((!_isOpera)||(_OperaRv>8.5))
    {
   this.hdr.onmousemove = new Function("e","this.grid.changeCursorState(e||window.event)");
      this.hdr.onmousedown = new Function("e","return this.grid.startColResize(e||window.event)");
    }
   this.obj.onmousemove = this._drawTooltip;
   this.obj.onclick = new Function("e","this.grid._doClick(e||window.event); if (this.grid._sclE) this.grid.editCell(e||window.event);  (e||event).cancelBubble=true; ");
   
   if (_isMacOS) {
	this.entBox.oncontextmenu = new Function("e","return this.grid._doContClick(e||window.event);");   
	}
   this.entBox.onmousedown = new Function("e","return this.grid._doContClick(e||window.event);");
   this.obj.ondblclick = new Function("e","if(!this.grid.wasDblClicked(e||window.event)){return false}; if (this.grid._dclE) this.grid.editCell(e||window.event);  (e||event).cancelBubble=true;");
   this.hdr.onclick = this._onHeaderClick;
   this.sortImg.onclick= function(){ self._onHeaderClick.apply({grid:self},[null,self.r_fldSorted]); };
   this.hdr.ondblclick = this._onHeaderDblClick;
   

   //VOID this.grid.ondblclick = this.onDoubleClick;
    if (!document.body._dhtmlxgrid_onkeydown){
      dhtmlxEvent(document,"keydown",new Function("e","if (globalActiveDHTMLGridObject) return globalActiveDHTMLGridObject.doKey(e||window.event);  return true;"));
      document.body._dhtmlxgrid_onkeydown=true;
    }

   dhtmlxEvent(document.body,"click",function(){ if (self.editStop) self.editStop();});

//nb:document.body.attachEvent("onclick",new Function("","if(this.document.getElementById('"+this.entBox.id+"').grid.isActive==-1)this.document.getElementById('"+this.entBox.id+"').grid.setActive(false)"))
   //activity management
    this.entBox.onbeforeactivate = new Function("","this._still_active=null; this.grid.setActive(); event.cancelBubble=true;");
   this.entBox.onbeforedeactivate = new Function("","if (this.grid._still_active) this.grid._still_active=null; else this.grid.isActive=false; event.cancelBubble=true;");
   //postprocessing events (method can be redeclared to react on some events during processing)
   this.doOnRowAdded = function(row){};
	if (this.entBox.style.height.toString().indexOf("%")!=-1)
    	this._setAutoResize();
  return this;
}


   /**
   *   @desc: detect is current grid is a treeGrid
   *   @type: private
   *   @topic: 2
   */
   dhtmlXGridObject.prototype.isTreeGrid=    function(){
        return (this.cellType._dhx_find("tree")!=-1);
    }

   /**
   *   @desc: adds row to the specified position (by default to the beginning of the grid)
   *   @param: new_id - id for new row
   *   @param: text - Array of values or String(with delimiter as in delimiter parameter)
   *   @param: [ind] - index of row (0 by default)
   *   @returns: new row dom object
   *   @type: public
   *   @topic: 2
   */
   dhtmlXGridObject.prototype.addRow=function(new_id,text,ind){
      var r =  this._addRow(new_id,text,ind);
      if (!this.dragContext)
      	this.callEvent("onRowAdded",[new_id]);
	  this.callEvent("onRowCreated",[r.idd,r,null]);
      if(this.pagingOn)
         this.changePage(this.currentPage)

      this.setSizes();
      r._added=true;

                       this.callEvent("onGridReconstructed",[]);

      return r;
   }


      /**
      *   @desc: first step of add row,  created a TR
      *   @type: private
      */
    dhtmlXGridObject.prototype._prepareRow=function(new_id){
                                var r=document.createElement("TR");
                        r.idd = new_id;
                        r.grid = this;

                        for(var i=0;i<this.hdr.rows[0].cells.length;i++){
                            var c = document.createElement("TD");
                                    //#cell_id:11052006{
                                    if (this._enbCid) c.id="c_"+r.idd+"_"+i;
                                    //#}
                                    c._cellIndex = i;
                                    if (this.dragAndDropOff) this.dragger.addDraggableItem(c,this);
                           if (this.cellAlign[i]) c.align = this.cellAlign[i];
                           c.style.verticalAlign = this.cellVAlign[i];
                           //add color to column
                           c.bgColor = this.columnColor[i] || "";

//#__pro_feature:21092006{
//#column_hidden:21092006{
                                    if ((this._hrrar)&&(this._hrrar[i]))
                                c.style.display="none";
//#}
//#}


                                    r.appendChild(c);
                                }
                                return r;
    }
      /**
      *   @desc: second step of add row,  fill tr with data
      *   @type: private
      */
    dhtmlXGridObject.prototype._fillRow=function(r,text){ 
        if (!this._parsing_) this.editStop();

        this.math_off=true;
        this.math_req=false;

        if(typeof(text)!='object')
           text = (text||"").split(this.delim);
        for(var i=0; i<r.childNodes.length; i++){
         if((i<text.length)||(this.defVal[i])){
	         var val = text[i]

         if (( this._dload && this.rowsAr[r.idd] ) || ( this._refresh_mode && (!this._fake || this._fake.rowsAr[r.idd] )))
                  var aeditor = this.cells3(r,r.childNodes[i]._cellIndex);
         else
                  var aeditor = this.cells4(r.childNodes[i]);

				if (aeditor.cell._cellIndex) val=text[aeditor.cell._cellIndex]
				if ((this.defVal[i])&&((val=="")||(typeof(val)=="undefined")))
                  val = this.defVal[i];

              aeditor.setValue(val)
              aeditor = aeditor.destructor();
           }else{
              var val = "&nbsp;";
              r.childNodes[i].innerHTML = val;
                       r.childNodes[i]._clearCell=true;
           }
        }
        this.math_off=false;
        if ((this.math_req)&&(!this._parsing_)){
               for(var i=0;i<this.hdr.rows[0].cells.length;i++)
                    this._checkSCL(r.childNodes[i]);
            this.math_req=false;
        }
        return r;
    }

      /**
      *   @desc: third step of add row,  attach TR to DOM
      *   @type: private
      */
    dhtmlXGridObject.prototype._insertRowAt=function(r,ind,skip){ 
             if ((ind<0)||((!ind)&&(parseInt(ind)!==0)))
                ind = this.rowsCol.length;
             else{
                if(ind>this.rowsCol.length)
                   ind = this.rowsCol.length;
             }    	
             
    		
    			
				if (this._cssEven){
                    if ((this._cssSP?this.getLevel(r.idd):ind)%2==1) r.className+=" "+this._cssUnEven+(this._cssSU?(this._cssUnEven+"_"+this.getLevel(r.idd)):"");
                    else r.className+=" "+this._cssEven+(this._cssSU?(" "+this._cssEven+"_"+this.getLevel(r.idd)):"");
                }                
			if (r._skipInsert) {                
				this.rowsAr[r.idd] = r;
    			return r;
    		}
                            if (!skip)
                            if ((ind==(this.obj.rows.length-1))||(!this.rowsCol[ind]))
                                if (_isKHTML)
                                    this.obj.appendChild(r);
                                else{
                                    this.obj.firstChild.appendChild(r);
                                    }
                            else
                                {
                                this.rowsCol[ind].parentNode.insertBefore(r,this.rowsCol[ind]);
                                }


                     this.rowsAr[r.idd] = r;
                     this.rowsCol._dhx_insertAt(ind,r);
                            if (this._cssEven){

                                if (!this._cssSP && (ind!=(this.rowsCol.length-1)))
                                    this._fixAlterCss(ind+1);
                            }

                     //this.chngCellWidth(ind)
                        this.doOnRowAdded(r);

                            //bad code, need to be rethinked
                            if ((this.math_req)&&(!this._parsing_)){
                                for(var i=0;i<this.hdr.rows[0].cells.length;i++)
                                   this._checkSCL(r.childNodes[i]);
                                this.math_req=false;
                            }

                            return r;
    }

   /**
   *   @desc: adds row to the specified position
   *   @param: new_id - id for new row
   *   @param: text - Array of values or String(with delimiter as in delimiter parameter)
   *   @param: [ind] - index of row (0 by default)
   *   @returns: new row dom object
   *   @type: private
   *   @topic: 2
   */
   dhtmlXGridObject.prototype._addRow   =    function(new_id,text,ind){ 
                       var row = this._fillRow(this._prepareRow(new_id),text);
                  if (!this._dload)                       
                  if ((ind>this.rowsCol.length && ind<(this.rowsCol.length+this.rowsBuffer[0].length)) || (typeof ind =="undefined" && this.rowsBuffer[0].length)){
                  	 if (typeof ind =="undefined") var inBufInd=this.rowsBuffer[0].length;
                  	 else var inBufInd = ind - this.rowsCol.length;
                     this.rowsBuffer[0]._dhx_insertAt(inBufInd,new_id);
                     this.rowsBuffer[1]._dhx_insertAt(inBufInd,row);
                     return row;
                  }
                  return this._insertRowAt(row,ind);
               }

/**
*   @desc: hide/show row (warning! - this command doesn't affect row indexes, only visual appearance)
*   @param: ind - column index
*   @param: state - true/false - hide/show row
*   @type:  public
*/
dhtmlXGridObject.prototype.setRowHidden=function(id,state){
    var f=convertStringToBoolean(state);
    //var ind=this.getRowIndex(id);
    //if (id<0)
   //   return;
    var row= this.getRowById(id)//this.rowsCol[ind];
   if(!row)
      return;

    if (row.expand==="")
        this.collapseKids(row);

    if ((state)&&(row.style.display!="none")){
        row.style.display="none";
        var z=this.selectedRows._dhx_find(row);
        if (z!=-1){
          row.className=row.className.replace("rowselected","");
            for (var i=0; i<row.childNodes.length; i++)
                row.childNodes[i].className=row.childNodes[i].className.replace(/cellselected/g,"");
             this.selectedRows._dhx_removeAt(z);
            }
                       this.callEvent("onGridReconstructed",[]);
        }

    if ((!state)&&(row.style.display=="none")){
        row.style.display="";
                       this.callEvent("onGridReconstructed",[]);
        }
   this.setSizes();
}

//#__pro_feature:21092006{
//#column_hidden:21092006{
/**
*   @desc: hide/show column
*   @param: ind - column index
*   @param: state - true/false - hide/show column
*   @type:  public
*   @edition: Professional
*/
   dhtmlXGridObject.prototype.setColumnHidden=function(ind,state){
   if (!this.hdr.rows.length){
   		if (!this._ivizcol) this._ivizcol=[];
   		return this._ivizcol[ind]=state;
   }
   
   
    if ((this.fldSorted)&&(this.fldSorted.cellIndex==ind)&&(state))
            this.sortImg.style.display = "none";

    var f=convertStringToBoolean(state);
    if (f){
        if (!this._hrrar) this._hrrar=new Array();
        else if (this._hrrar[ind]) return;
            this._hrrar[ind]="display:none;";
            this._hideShowColumn(ind,"none");
    }
    else
    {
        if ((!this._hrrar)||(!this._hrrar[ind])) return;
        this._hrrar[ind]="";
        this._hideShowColumn(ind,"");
    }

    if ((this.fldSorted)&&(this.fldSorted.cellIndex==ind)&&(!state))
            this.sortImg.style.display = "inline";
}



/**
*   @desc: get show/hidden status of column
*   @param: ind - column index
*   @type:  public
*   @edition: Professional
*   @returns:  if column hidden then true else false
*/
dhtmlXGridObject.prototype.isColumnHidden=function(ind){
     if ((this._hrrar)&&(this._hrrar[ind])) return true;
     return false;
}


/**
*   @desc: set list of visible/hidden columns
*   @param: list - list of true/false separated by comma
*   @type:  public
*   @edition: Professional
*   @topic:0
*/
dhtmlXGridObject.prototype.setColumnsVisibility=function(list){
	this.setColHidden(list)
}
/**
*   @desc: set list of visible/hidden columns
*   @param: list - list of true/false separated by comma
*   @type:  deprecated
*	@newmethod: setColumnsVisibility
*   @edition: Professional
*   @topic:0
*/
dhtmlXGridObject.prototype.setColHidden=function(list){
    if (list) this._ivizcol=list.split(",");
    
   if (this.hdr.rows.length && this._ivizcol)
   for (var i=0; i<this._ivizcol.length; i++)
       this.setColumnHidden(i,this._ivizcol[i]);

}

      /**
      *   @desc: fix hidden state for column in all rows
      *   @type: private
      */
dhtmlXGridObject.prototype._fixHiddenRowsAll=function(pb,ind,prop,state){
 var z=pb.rows.length;
 for(var i=0;i<z;i++){
	var x=pb.rows[i].cells;
	if (x.length!=this._cCount){
		for (var j=0; j<x.length; j++)
			if (x[j]._cellIndex==ind){
            	x[j].style[prop]=state;
            	break;
			}
	}
    else 
    	x[ind].style[prop]=state;
 }
}
/**
*   @desc: hide column
*   @param: ind - column index
*   @param: state - hide/show
*   @edition: Professional
*   @type:  private
*/
dhtmlXGridObject.prototype._hideShowColumn=function(ind,state){
   var hind=ind;
   if ((this.hdr.rows[1]._childIndexes)&&(this.hdr.rows[1]._childIndexes[ind]!=ind))
      hind=this.hdr.rows[1]._childIndexes[ind];

    if (state=="none"){
        this.hdr.rows[0].cells[ind]._oldWidth = this.hdr.rows[0].cells[ind].style.width;
        this.hdr.rows[0].cells[ind]._oldWidthP = this.cellWidthPC[ind];
        this.obj.rows[0].cells[ind].style.width = "0px";
		
        this._fixHiddenRowsAll(this.obj,ind,"display","none");
      if (this._fixHiddenRowsAllTG) this._fixHiddenRowsAllTG(ind,"none");
      
        if ((_isOpera&&_OperaRv<9)||_isKHTML||(_isFF)){
         this._fixHiddenRowsAll(this.hdr,ind,"display","none");
        if (this.ftr)
            this._fixHiddenRowsAll(this.ftr.childNodes[0],ind,"display","none");
	    }

			this._fixHiddenRowsAll(this.hdr,ind,"whiteSpace","nowrap");

			if (!this.cellWidthPX.length && !this.cellWidthPC.length)
				this.cellWidthPX=[].concat(this.initCellWidth);
			
            if (this.cellWidthPX[ind]) this.cellWidthPX[ind]=0;
            if (this.cellWidthPC[ind]) this.cellWidthPC[ind]=0;
        }
    else {
        if (this.hdr.rows[0].cells[ind]._oldWidth){
        var zrow=this.hdr.rows[0].cells[ind];
          if (_isOpera||_isKHTML||(_isFF))
             this._fixHiddenRowsAll(this.hdr,ind,"display","");

         if (this.ftr)
            this._fixHiddenRowsAll(this.ftr.childNodes[0],ind,"display","");

             this.obj.rows[0].cells[ind].style.width = this.hdr.rows[0].cells[ind]._oldWidth;
             this._fixHiddenRowsAll(this.obj,ind,"display","");
         if (this._fixHiddenRowsAllTG) this._fixHiddenRowsAllTG(ind,"");          

             zrow.style.width = zrow._oldWidth;

			this._fixHiddenRowsAll(this.hdr,ind,"whiteSpace","normal");
             
             if (zrow._oldWidthP) this.cellWidthPC[ind]=zrow._oldWidthP;
             if (zrow._oldWidth) this.cellWidthPX[ind]=parseInt(zrow._oldWidth);
        }
    }
    this.setSizes();
	
    if ((!_isIE)&&(!_isFF))
    {
    //dummy Opera/Safari fix
    this.obj.border=1;
    this.obj.border=0;
    }

}

//#}

//#colspan:20092006{
/**
*   @desc: enable/disable colspan support
*   @param: mode - true/false
*   @type:  public
*   @edition: Professional
*/
 dhtmlXGridObject.prototype.enableColSpan=function(mode){
    this._ecspn=convertStringToBoolean(mode);
 }
 /**
*   @desc: enable/disable colspan support
*   @param: mode - true/false
*   @type:  deprecated
*	@newmethod: enableColSpan
*   @edition: Professional
*/
 dhtmlXGridObject.prototype.enableCollSpan=function(mode){
    this._ecspn=convertStringToBoolean(mode);
 }
 //#}

 //#}
/**
*   @desc: enable/disable hovering row on mouse over
*   @param: mode - true/false
*   @param: cssClass - css class for hovering row
*   @type:  public
*/
dhtmlXGridObject.prototype.enableRowsHover = function(mode,cssClass){
    this._hvrCss=cssClass;
    if (convertStringToBoolean(mode)){
        if (!this._elmnh){
             this.obj._honmousemove=this.obj.onmousemove;
             this.obj.onmousemove=this._setRowHover;
             if (_isIE)
                this.obj.onmouseleave=this._unsetRowHover;
             else
                 this.obj.onmouseout=this._unsetRowHover ;

             this._elmnh=true;
        }
    } else {
        if (this._elmnh){
             this.obj.onmousemove=this.obj._honmousemove;
             if (_isIE)
                this.obj.onmouseleave=null;
             else
                 this.obj.onmouseout=null;

             this._elmnh=false;
        }
    }
};

/**
*   @desc: enable/disable events which fire excell editing, mutual exclusive with enableLightMouseNavigation
*   @param: click - true/false - enable/disable editing by single click
*   @param: dblclick - true/false - enable/disable editing by double click
*   @param: f2Key - enable/disable editing by pressing F2 key
*   @type:  public
*/
dhtmlXGridObject.prototype.enableEditEvents = function(click, dblclick, f2Key){
         this._sclE = convertStringToBoolean(click);
         this._dclE = convertStringToBoolean(dblclick);
         this._f2kE = convertStringToBoolean(f2Key);
}


/**
*   @desc: enable/disable light mouse navigation mode (row selection with mouse over, editing with single click), mutual exclusive with enableEditEvents
*   @param: mode - true/false
*   @type:  public
*/
dhtmlXGridObject.prototype.enableLightMouseNavigation = function(mode){
    if (convertStringToBoolean(mode)){
        if (!this._elmn){
             this.entBox._onclick=this.entBox.onclick;
             this.entBox.onclick = function () {return true; };
			 
			 this.obj._onclick=this.obj.onclick;
             this.obj.onclick=function (e){
                 var c = this.grid.getFirstParentOfType(e?e.target:event.srcElement,'TD');
                 this.grid.editStop();
                 this.grid.doClick(c);
                this.grid.editCell();
             (e||event).cancelBubble=true;
                 }

             this.obj._onmousemove=this.obj.onmousemove;
             this.obj.onmousemove=this._autoMoveSelect;
             this._elmn=true;
        }
    } else {
        if (this._elmn){
             this.entBox.onclick = this.entBox._onclick;
             this.obj.onclick=this.obj._onclick;
             this.obj.onmousemove=this.obj._onmousemove;
             this._elmn=false;
        }
    }
}


/**
*   @desc: remove hover state on row
*   @type:  private
*/
dhtmlXGridObject.prototype._unsetRowHover = function(e,c){
        if (c) that=this; else that=this.grid;

        if ((that._lahRw)&&(that._lahRw!=c)){
         for(var i=0;i<that._lahRw.childNodes.length;i++)
                that._lahRw.childNodes[i].className=that._lahRw.childNodes[i].className.replace(that._hvrCss,"");
            that._lahRw=null;
        }
}

/**
*   @desc: set hover state on row
*   @type:  private
*/
dhtmlXGridObject.prototype._setRowHover = function(e){
        var c = this.grid.getFirstParentOfType(e?e.target:event.srcElement,'TD');
        if (c) {
            this.grid._unsetRowHover(0,c);
            c=c.parentNode;
         for(var i=0;i<c.childNodes.length;i++)
                c.childNodes[i].className+=" "+this.grid._hvrCss;
            this.grid._lahRw=c;
        }
        this._honmousemove(e);
}

/**
*   @desc: onmousemove, used in light mouse navigaion mode
*   @type:  private
*/
dhtmlXGridObject.prototype._autoMoveSelect = function(e){
    //this - grid.obj
    if(!this.grid.editor)
    {
        var c = this.grid.getFirstParentOfType(e?e.target:event.srcElement,'TD');
      if (c.parentNode.idd)
           this.grid.doClick(c,true,0);
    }
    this._onmousemove(e);
}

//#__pro_feature:21092006{
//#distrb_parsing:21092006{
/**
*   @desc: enable/disable distributed parsing (rows paresed portion by portion with some timeout)
*   @param: mode - true/false
*   @param: count - count of nodes parsed by one step (the 10 by default)
*   @param: time - time between parsing counts in milli seconds (the 250 by default)
*   @type:  public
*   @edition: Professional
*/
dhtmlXGridObject.prototype.enableDistributedParsing = function(mode,count,time){
    count=count||10;
    time=time||250;
    if (convertStringToBoolean(mode)){
        this._ads_count=count;
        this._ads_time=time;
    }
    else  this._ads_count=0;
}


/**
*   @desc:  call function from saved context, used in distributed parsing
*   @type:  private
*/
function _contextCall(obj,name,rowsCol,startIndex,tree,pId,i,n){
    obj._contextCallTimer=window.setTimeout(function(){
        var res=obj[name](rowsCol,startIndex,tree,pId,i);
        if (obj._ahgr) obj.setSizes();
        if (res!=-1)
            obj.callEvent("onXLE",[obj,obj.rowsCol.length]);
    },n);
    return this;
}
//#}
//#}
      /**
          *     @desc: destructor, removes grid and cleans used memory
          *     @type: public
        *     @topic: 0
          */
dhtmlXGridObject.prototype.destructor=function(){
    if (this._sizeTime)
        this._sizeTime=window.clearTimeout(this._sizeTime);
		
    var a;
    this.xmlLoader=this.xmlLoader.destructor();
    for (var i=0; i<this.rowsCol.length; i++)
        if (this.rowsCol[i]) this.rowsCol[i].grid=null;
    for (i in this.rowsAr)
        if (this.rowsAr[i])     	
        	this.rowsAr[i]=null;

    this.rowsCol=new dhtmlxArray();
    this.rowsAr=new Array();
    this.entBox.innerHTML="";
   this.entBox.onclick = function(){};
   this.entBox.onmousedown = function(){};
   this.entBox.onbeforeactivate = function(){};
   this.entBox.onbeforedeactivate = function(){};
   this.entBox.onbeforedeactivate = function(){};

   this.entBox.onselectstart = function(){};
   this.entBox.grid = null;


    for (a in this){
        if ((this[a])&&(this[a].m_obj))
            this[a].m_obj=null;
        this[a]=null;
        }


    if (this==globalActiveDHTMLGridObject)
        globalActiveDHTMLGridObject=null;
//   self=null;
    return null;
}





/**
*     @desc: get sorting state of grid
*     @type: public
*     @returns: array, first element is index of sortef column, second - direction of sorting ("asc" or "des").
*     @topic: 0
*/
   dhtmlXGridObject.prototype.getSortingState=function(){
                var z=new Array();
                if (this.fldSorted){
                    z[0]=this.fldSorted._cellIndex;
                    z[1]=(this.sortImg.src.indexOf("sort_desc.gif")!=-1)?"des":"asc";
                }
                return z;
    };

/**
*     @desc: enable autoheight of grid
*     @param: mode - true/false
*     @param: maxHeight - maximum height before scrolling appears (no limit by default)
*     @param: countFullHeight - control the usage of maxHeight parameter - when set to true all grid height included in max height calculation, if false then only data part (no header) of grid included in calcualation (false by default)
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableAutoHeight=function(mode,maxHeight,countFullHeight){
        this._ahgr=convertStringToBoolean(mode);
        this._ahgrF=convertStringToBoolean(countFullHeight);
        this._ahgrM=maxHeight||null;
      if (maxHeight=="auto")
         {
         this._ahgrM=null;
         this._ahgrMA=true;
         this._setAutoResize();
      //   this._activeResize();
         }
    };
   dhtmlXGridObject.prototype.enableAutoHeigth=dhtmlXGridObject.prototype.enableAutoHeight;

/**
*     @desc: enable stable sorting (slow). Stable sorting algorithms maintain the relative order of records with equal keys
*     @param: mode - true/false
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableStableSorting=function(mode){
		this._sst=convertStringToBoolean(mode);
		this.rowsCol.stablesort=function(cmp){
      	 var size=this.length-1;
         for (var i=0; i<this.length-1; i++){
            for (var j=0; j<size; j++)
               if (cmp(this[j],this[j+1])>0){
                  var temp=this[j];
                  this[j]=this[j+1];
                  this[j+1]=temp;
               }
               size--;
           }
        }
    };

/**
*     @desc: enable/disable hot keys in grid
*     @param: mode - true/false
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableKeyboardSupport=function(mode){
        this._htkebl=!convertStringToBoolean(mode);
    };


/**
*     @desc: enable/disable context menu
*     @param: dhtmlxMenu object, if null - context menu will be disabled
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableContextMenu=function(menu){
        this._ctmndx=menu;
    };
/**
*     @desc: set event handler, which will be called immideatly before showing context menu
*     @param: func - user defined function
*     @type: deprecated
*     @event: onBeforeContextMenu
*     @eventdesc: Event raised immideatly before showing context menu
*     @eventparam:  ID of clicked row
*     @eventparam:  index of cell column
*     @eventparam:  grid object
*     @eventreturns: if event returns false, then context menu is not shown
*     @topic: 0,10
*/
   dhtmlXGridObject.prototype.setOnBeforeContextMenu=function(func){
            this.attachEvent("onBeforeContextMenu",func);
    };

/**
*     @desc: set event handler, which will be called immideatly after right mouse button click on grid row
*     @param: func - user defined function
*     @type: deprecated
*     @event: onRightClick
*     @eventdesc: Event raised immideatly after right mouse button clicked on grid row
*     @eventparam:  ID of clicked row
*     @eventparam:  index of cell column
*     @eventparam:  event object
*     @eventreturns: if event returns false, then dhtmlxMenu integration disabled
*     @topic: 0,10
*/
dhtmlXGridObject.prototype.setOnRightClick=function(func){
   this.attachEvent("onRightClick",func);
};



/**
*     @desc: set width of browser scrollbars, will be used to correct autoWidth calculations (by default grid uses 16 for IE and 19 pixels for FF)
*     @param: width - scrollbar width
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.setScrollbarWidthCorrection=function(width){
        this._scrFix=parseInt(width);
    };

/**
*     @desc: enable/disable tooltips for specified colums
*     @param: list - list of true/false values, tooltips enabled for all columns by default
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableTooltips=function(list){
        this._enbTts=list.split(",");
        for (var i=0; i<this._enbTts.length; i++)
            this._enbTts[i]=convertStringToBoolean(this._enbTts[i]);
    };


/**
*     @desc: enable/disable resizing for specified colums
*     @param: list - list of true/false values, resizing enabled for all columns by default
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableResizing=function(list){
        this._drsclmn=list.split(",");
        for (var i=0; i<this._drsclmn.length; i++)
            this._drsclmn[i]=convertStringToBoolean(this._drsclmn[i]);
    };

/**
*     @desc: set minimum column width ( works only for manual resizing )
*     @param: width - minimum column width, can be set for specified column, or as comma separated list for all columns
*     @param: ind - column index
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.setColumnMinWidth=function(width,ind){
        if (arguments.length==2){
            if (!this._drsclmW) this._drsclmW=new Array();
            this._drsclmW[ind]=width;
            }
        else
            this._drsclmW=width.split(",");
    };


//#cell_id:11052006{
/**
*     @desc: enable/disable unique id for cells (id will be automaticaly created using the following template: "c_[RowId]_[colIndex]")
*     @param: mode - true/false - enable/disable
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.enableCellIds=function(mode){
        this._enbCid=convertStringToBoolean(mode);
    };
//#}



//#locked_row:11052006{
/**
*     @desc: lock/unlock row for editing
*     @param: rowId - id of row
*     @param: mode - true/false - lock/unlock
*     @type: public
*     @topic: 0
*/
   dhtmlXGridObject.prototype.lockRow=function(rowId,mode){
        var z=this.getRowById(rowId);
        if (z) {
            z._locked=convertStringToBoolean(mode);
            if ((this.cell)&&(this.cell.parentNode.idd==rowId))
                this.editStop();
            }
    };
//#}

/**
*   @desc:  get values of all cells in row
*   @type:  private
*/
   dhtmlXGridObject.prototype._getRowArray=function(row){
        var text=new Array();
        for (var ii=0; ii<row.childNodes.length; ii++){
			var a=this.cells3(row,ii);
			if (a.cell._code) text[ii]=a.cell._val;
			else text[ii]=a.getValue();
		}
        return text;
        }

//#__pro_feature:21092006{
//#data_format:12052006{
/**
*     @desc: set mask for date formatting in cell
*     @param: mask - date mask, d,m,y will mean day,month,year; for example "d/m/y" - 22/05/1985
*     @type: public
*     @edition: Professional
*     @topic: 0
*/
   dhtmlXGridObject.prototype.setDateFormat=function(mask){
        this._dtmask=mask;
    }

/**
*     @desc: set mask for formatting numeric data ( works for [ed/ro]n excell only or oher cell types with suport for this method)
*     @param: mask - numeric mask; for example 0,000.00 - 1,234.56
*     @param: cInd - column index
*     @param: p_sep - char used as groups separator ( comma by default )
*     @param: d_sep - char used as decimal part separator ( point by default )
*     @type: public
*     @edition: Professional
*     @topic: 0
*/
   dhtmlXGridObject.prototype.setNumberFormat=function(mask,cInd,p_sep,d_sep){
            var nmask=mask.replace(/[^0\,\.]*/g,"");
            var pfix=nmask.indexOf(".");
            if (pfix>-1) pfix=nmask.length-pfix-1;
            var dfix=nmask.indexOf(",");
            if (dfix>-1) dfix=nmask.length-pfix-2-dfix;

            p_sep=p_sep||".";
            d_sep=d_sep||",";
            var pref=mask.split(nmask)[0];
            var postf=mask.split(nmask)[1];
            this._maskArr[cInd]=[pfix,dfix,pref,postf,p_sep,d_sep];
    }
/**
*   @desc:  convert formated value to original
*   @type:  private
*/
    dhtmlXGridObject.prototype._aplNFb=function(data,ind){
            var a=this._maskArr[ind];
            if (!a) return data;

            var ndata=parseFloat(data.toString().replace(/[^0-9]*/g,""));
            if (data.toString().substr(0,1)=="-") ndata=ndata*-1;
            if (a[0]>0) ndata=ndata/Math.pow(10,a[0]);
            return ndata;
    }

/**
*   @desc:  format data with mask
*   @type:  private
*/
   dhtmlXGridObject.prototype._aplNF=function(data,ind){
            var a=this._maskArr[ind];
            if (!a) return data;

            var c=(parseFloat(data)<0?"-":"")+a[2];
            data = Math.abs(Math.round(parseFloat(data)*Math.pow(10,a[0]>0?a[0]:0))).toString();
            data=(data.length<a[0]?Math.pow(10,a[0]+1-data.length).toString().substr(1,a[0]+1)+data.toString():data).split("").reverse();
            data[a[0]]=(data[a[0]]||"0")+a[4];
            if (a[1]>0)  for (var j=(a[0]>0?0:1)+a[0]+a[1]; j<data.length; j+=a[1]) data[j]+=a[5];
            return c+data.reverse().join("")+a[3];
    }
//#} 

//#}

//#config_from_xml:20092006{

/**
*   @desc:  configure grid structure from XML
*   @type:  private
*/
      dhtmlXGridObject.prototype._launchCommands = function(arr){
         for (var i=0; i<arr.length; i++){
            var args=new Array();
            for (var j=0; j<arr[i].childNodes.length; j++)
               if (arr[i].childNodes[j].nodeType==1)
                  args[args.length]=arr[i].childNodes[j].firstChild.data;
            this[arr[i].getAttribute("command")].apply(this,args);
         }
     }


/**
*   @desc:  configure grid structure from XML
*   @type:  private
*/
      dhtmlXGridObject.prototype._parseHead = function(xmlDoc){
                    var hheadCol = this.xmlLoader.doXPath("//rows/head",xmlDoc);
                    if (hheadCol.length){
                        
                          var headCol = this.xmlLoader.doXPath("//rows/head/column",hheadCol[0]);
                                var asettings = this.xmlLoader.doXPath("//rows/head/settings",hheadCol[0]);
                                var awidthmet="setInitWidths";
                                var split=false;

                                if (asettings[0]){
                                    for (var s=0; s<asettings[0].childNodes.length; s++)
                                        switch (asettings[0].childNodes[s].tagName){
                                            case "colwidth":
                                                if (asettings[0].childNodes[s].firstChild && asettings[0].childNodes[s].firstChild.data=="%")
                                                    awidthmet="setInitWidthsP";
                                                break;
                                            case "splitat":
                                                split=(asettings[0].childNodes[s].firstChild?asettings[0].childNodes[s].firstChild.data:false);
                                                break;
                                        }
                                }
                    this._launchCommands(this.xmlLoader.doXPath("//rows/head/beforeInit/call",hheadCol[0]));
                   
                          if(headCol.length>0){
                            var sets=[[],[],[],[],[],[],[],[],[]];
                            var attrs=["","width","type","align","sort","color","format","hidden","id"];
                            var calls=["setHeader",awidthmet,"setColTypes","setColAlign","setColSorting","setColumnColor","","","setColumnIds"];
                            for (var i=0; i < headCol.length; i++) {
                            	for (var j=1; j < attrs.length; j++) 
                            		sets[j].push(headCol[i].getAttribute(attrs[j]));
                            	sets[0].push((headCol[i].firstChild?headCol[i].firstChild.data:"").replace(/^\s*((.|\n)*.+)\s*$/gi,"$1"));
                            };

                            for (var i=0; i < calls.length; i++) 
                            	if (calls[i]) this[calls[i]](sets[i].join(this.delim))
                            
                            for (var i=0; i<headCol.length; i++){
                            	if ((this.cellType[i].indexOf('co')==0)||(this.cellType[i]=="clist")){
                                	var optCol = this.xmlLoader.doXPath("./option",headCol[i]);
                                    if (optCol.length){
                                    	var resAr=new Array();
                                        if (this.cellType[i]=="clist"){
                                        	for (var j=0;j<optCol.length; j++)
                                            	resAr[resAr.length]=optCol[j].firstChild?optCol[j].firstChild.data:"";
                                            this.registerCList(i,resAr);
                                        }
                                        else{
                                        	var combo=this.getCombo(i);
                                            for (var j=0;j<optCol.length; j++)
                                            	combo.put(optCol[j].getAttribute("value"),optCol[j].firstChild?optCol[j].firstChild.data:"");
                                        }
                                    }
                                }
								else
                                	if (sets[6][i])
                                    	if ((this.cellType[i]=="calendar")||(this.fldSort[i]=="date"))
                                     		this.setDateFormat(sets[6][i],i);
                                  		else
                                     		this.setNumberFormat(sets[6][i],i);
                            }

							this.init();
							if (this.setColHidden)
                            	this.setColHidden(sets[7].join(this.delim));
                            if ((split)&&(this.splitAt)) this.splitAt(split);
            	}
            	this._launchCommands(this.xmlLoader.doXPath("//rows/head/afterInit/call",hheadCol[0]));
			}
                        //global(grid) user data
                        var gudCol = this.xmlLoader.doXPath("//rows/userdata",xmlDoc);
                        if(gudCol.length>0){
						   if (!this.UserData["gridglobaluserdata"])
                           		this.UserData["gridglobaluserdata"] = new Hashtable();
                           for(var j=0;j<gudCol.length;j++){
                              this.UserData["gridglobaluserdata"].put(gudCol[j].getAttribute("name"),gudCol[j].firstChild?gudCol[j].firstChild.data:"");
                           }
                        }            
        }
    
    
//#}


   /**
      *    @desc: populate grid with data from xml file (if passed parameter contains '.') or data island
      *    @param: [xml] - xml island will be found by grid id ([id]_xml) if no file or island id is specified. This also can be ready-to-use XML object
      *   @param: [startIndex] - index of row in grid to start insertion from
      *   @type: public
      *   @topic: 2,5
      */
      dhtmlXGridObject.prototype.parseXML = function(xml,startIndex){
                   this._xml_ready=true;
                   var pid=null;
                   var zpid=null;
                        if(!xml)
                           try{
                              var xmlDoc = eval(this.entBox.id+"_xml").XMLDocument;
                           }catch(er){
                              var xmlDoc = this.loadXML(this.xmlFileUrl)
                           }
                        else{
                           if(typeof(xml)=="object"){
                              var xmlDoc = xml;
                           }else{
                              if(xml.indexOf(".")!=-1){
                                 if(this.xmlFileUrl=="")
                                    this.xmlFileUrl = xml
                                 var xmlDoc = this.loadXML(xml)
                                            return;
                              }else
                                 var xmlDoc = (_isIE?eval(xml).XMLDocument:document.getElementById(xml));
                           }
                        }





                        var ar = new Array();
                        var idAr = new Array();

						var a_top=this.xmlLoader.doXPath("//rows",xmlDoc);
						
						if (a_top[0] && a_top[0].getAttribute("total_count"))
							this.limit=a_top[0].getAttribute("total_count");
							
//#config_from_xml:20092006{
						this._parseHead(xmlDoc);
//#}


                        

                        var tree=this.cellType._dhx_find("tree");
                        var rowsCol = this.xmlLoader.doXPath("//rows/row",xmlDoc);
                        if(rowsCol.length==0){
                           this.recordsNoMore = true;
                     var top=this.xmlLoader.doXPath("//rows",xmlDoc);
                     		if (!top) return;
                            var pid=(top[0].getAttribute("parent")||0);
                          if ((tree!=-1)&&(this.rowsAr[pid])){
                        var tree_r=this.rowsAr[pid].childNodes[tree];
                     }
                        }
                                else{
                                    pid=(rowsCol[0].parentNode.getAttribute("parent")||null);
                                    zpid=this.getRowById(pid);
                                    if (zpid) zpid._xml_await=false;
                                    else pid=null;
                                    startIndex=this.getRowIndex(pid)+1;
                                }



                        //rows
                                if (tree==-1) tree=this.cellType._dhx_find("3d");
                                if (this._innerParse(rowsCol,startIndex,tree,pid)==-1) return (this._ahgr?this.setSizes():"");
                                if (zpid) this.expandKids(zpid);

                        

                                if (tree!=-1){
                                  var oCol = this.xmlLoader.doXPath("//row[@open]",xmlDoc);
                                for (var i=0; i<oCol.length; i++)
                                    this.openItem(oCol[i].getAttribute("id"));
                                    }

                              this.setSizes();
                            if (_isOpera){
                                this.obj.style.border=1;
                                this.obj.style.border=0;
                                }
                            this._startXMLLoading=false;

                            this.callEvent("onXLE",[this,rowsCol.length,pid,xmlDoc]);
                            
                  }
/**
*   @desc:  add additional attributes to row, based on XML attributes
*   @type:  private
*/
         dhtmlXGridObject.prototype._postRowProcessing=function(r,xml){
               var rId = xml.getAttribute("id");
               var xstyle = xml.getAttribute("style");

                //user data
              var udCol = this.xmlLoader.doXPath("./userdata",xml);
              if(udCol.length>0){
			  	 if (!this.UserData[rId])
	                 this.UserData[rId] = new Hashtable();
                 for(var j=0;j<udCol.length;j++){
                    this.UserData[rId].put(udCol[j].getAttribute("name"),udCol[j].firstChild?udCol[j].firstChild.data:"");
                 }
              }

                //#td_tr_classes:06062006{
                var css1=xml.getAttribute("class");
                if (css1) r.className+=(r._css=" "+css1);
                //#}
                var css1=xml.getAttribute("bgColor");
            if (css1)
               for (var i=0; i<r.childNodes.length; i++)
                  r.childNodes[i].bgColor=css1;
                  
                //#locked_row:11052006{
                if (xml.getAttribute("locked"))
                {
                    r._locked=true;
                }
                //#}


                //select row
                if(xml.getAttribute("selected")==true){
                    this.setSelectedRow(rId,this.selMultiRows,false,xml.getAttribute("call")==true)
                }
                /*
                //expand row
                if(xml.getAttribute("expand")=="1"){
                    r.expand = "";
                }
                */

                if (xstyle) this.setRowTextStyle(rId,xstyle);

			this.callEvent("onRowCreated",[r.idd,r,xml]);
         }
/**
*   @desc:  fill row with data from XML
*   @type:  private
*/
         dhtmlXGridObject.prototype._fillRowFromXML=function(r,xml,tree,pId){
            var cellsCol = this.xmlLoader.doXPath("./cell",xml);
            var strAr = new Array(0);

            for(var j=0;j<cellsCol.length;j++){
            var cellVal=cellsCol[j];
            var exc=cellVal.getAttribute("type");
//#__pro_feature:21092006{
//#xml_content:23102006{
               if (cellVal.getAttribute("xmlcontent"))
                  cellVal=cellsCol[j];
               else
//#}
//#}
               if (cellVal.firstChild)
                  cellVal=cellVal.firstChild.data;
            else cellVal="";
                if (j!=tree)
                    strAr[strAr.length] = cellVal;
                else
                    strAr[strAr.length] = [pId,cellVal,((xml.getAttribute("xmlkids")||r._xml)?"1":"0"),(cellsCol[j].getAttribute("image")||"leaf.gif")];

            if (exc)
               r.childNodes[j]._cellType=exc;

           }
         if (this._c_order) strAr=this._swapColumns(strAr);
            for(var j=0;j<cellsCol.length;j++){
            	var ji=r._childIndexes?r._childIndexes[j]:j;
               	 var css1=cellsCol[j].getAttribute("class");
                 if (css1) r.childNodes[ji].className=css1;
				 css1=cellsCol[j].getAttribute("style");
                 if (css1) r.childNodes[ji].style.cssText+=";"+css1;
                 css1=cellsCol[j].getAttribute("title");
                 if (css1) r.childNodes[ji].title=css1;
            }
            this._fillRow(r,strAr);
//#__pro_feature:21092006{
//#colspan:20092006{
            if (this._ecspn && !this._refresh_mode)
            {
                r._childIndexes=new Array();
                var col_ex=0;
                var l=this.obj.rows[0].childNodes.length
                for(var j=0;j<l;j++){
                    r._childIndexes[j]=j-col_ex;
                    if (!cellsCol[j]) continue;
                    var col=cellsCol[j].getAttribute("colspan");
                    if (col){
                    r.childNodes[j-col_ex].colSpan=col;
                    for (var z=1; z<col; z++){
                        r.removeChild(r.childNodes[j-col_ex+1]);
                        r._childIndexes[j+z]=j-col_ex;
                        }
                    col_ex+=(col-1);
                    j+=(col-1);
                  }
                }
                if (!col_ex)
                   r._childIndexes=null;

            }
//#}
//#}
         if ((r.parentNode)&&(r.parentNode.tagName))
            this._postRowProcessing(r,xml);
		 if (this._customAttrs) this._customAttrs(r.idd,cellsCol)
            return r;
         }


/**
*   @desc:  inner recursive part of XML parsing routine, parses xml for one branch of treegrid or for whole grid
*   @type:  private
*/
         dhtmlXGridObject.prototype._innerParse=function(rowsCol,startIndex,tree,pId,i){
                            i=i||0;    var imax=i+this._ads_count*1;
                            var r=null;
                     var rowsCol2;
                            for(var i;i<rowsCol.length;i++){
//#__pro_feature:21092006{
//#distrb_parsing:21092006{
                                    if (this._ads_count && i==imax) {
                                        new _contextCall(this,"_innerParse",rowsCol,startIndex,tree,pId,i,this._ads_time);
                                        return -1;
                                        }
//#}
//#}
                     if ((pId)||(i<this.rowsBufferOutSize || this.rowsBufferOutSize==0)){

                               this._parsing_=true;
                                var rId = (rowsCol[i].getAttribute("id")||(this.rowsCol.length+2));
                        r=this._prepareRow(rId);

                        if (tree!=-1){
                           rowsCol2 = this.xmlLoader.doXPath("./row",rowsCol[i]);
                           if ((rowsCol2.length!=0)&&(this._slowParse))
                                    r._xml=rowsCol2;
                        }

                                r=this._fillRowFromXML(r,rowsCol[i],tree,pId);

							
                               if(startIndex){
                                 r = this._insertRowAt(r,startIndex);
                                   startIndex++;
                               }else{
                                  r = this._insertRowAt(r);
                               }
                          this._postRowProcessing(r,rowsCol[i]);
                                 this._parsing_=false;
                            }
                     else{
                               var len = this.rowsBuffer[0].length
                               this.rowsBuffer[1][len] = rowsCol[i];
                               this.rowsBuffer[0][len] = rowsCol[i].getAttribute("id")
                               if (!this.rowsBuffer[0][len]){
                               		this.rowsBuffer[0][len]=this.rowsCol.length+2+len;
                               		rowsCol[i].setAttribute("id",this.rowsBuffer[0][len])
                           	   }
                            }

                            if ((tree!=-1)&&(rowsCol2.length!=0)&&(!this._slowParse))
                                startIndex=this._innerParse(rowsCol2,startIndex,tree,rId);

               }

                //nb:paging
                if(this.pagingOn && this.rowsBuffer[0].length>0){
                    this.changePage(this.currentPage)
                }

                if ((r)&&(this._checkSCL))
                    for(var i=0;i<this.hdr.rows[0].cells.length;i++)
                        this._checkSCL(r.childNodes[i]);
                return startIndex;
            }


      /**
      *   @desc: get list of Ids of all rows with checked exCell in specified column
      *   @type: public
      *   @param: col_ind - column index
      *   @topic: 5
      */
 dhtmlXGridObject.prototype.getCheckedRows=function(col_ind){
    var d=new Array();
    this.forEachRow(function(id){
    	if (this.cells(id,col_ind).getValue()!=0)
    		d.push(id);
    })
    return d.join(",");
 }
/**
*   @desc:  grid body onmouseover function
*   @type:  private
*/
 dhtmlXGridObject.prototype._drawTooltip=function(e){
    var c = this.grid.getFirstParentOfType(e?e.target:event.srcElement,'TD');
    if((this.grid.editor)&&(this.grid.editor.cell==c)) return true;

    var r = c.parentNode;
    if (!r.idd) return;
    var el=(e?e.target:event.srcElement);
    if (r.idd==window.unknown) return true;
	if (!this.grid.callEvent("onMouseOver",[r.idd,c._cellIndex])) return true;
    if ((this.grid._enbTts)&&(!this.grid._enbTts[c._cellIndex])) {
    	if (el.title) el.title='';
        return true; }
    var ced = this.grid.cells(r.idd,c._cellIndex);
	if (el._title) ced.cell.title="";
	if (!ced.cell.title) el._title=true;
    if (ced)
        el.title=ced.cell.title||(ced.getTitle?ced.getTitle():(ced.getValue()||"").toString().replace(/<[^>]*>/gi,""));

    return true;
    };

/**
*   @desc:  can be used for setting correction for cell padding, while calculation setSizes
*   @type:  private
*/
 dhtmlXGridObject.prototype.enableCellWidthCorrection=function(size){
    if (_isFF) this._wcorr=parseInt(size);
 }


 	/**
	*	@desc: gets a list of all row ids in grid
	*	@param: separator - delimiter to use in list
	*	@returns: list of all row ids in grid
	*	@type: public
	*	@topic: 2,7
	*/
dhtmlXGridObject.prototype.getAllRowIds = function(separator){
							var ar = new Array(0)
                            var z=this.getRowsNum();
							for(i=0;i<z;i++)
                                if ((this.rowsCol[i])&&(!this.rowsCol[i]._sRow)&&(!this.rowsCol[i]._rLoad))
                                   ar[ar.length]=this.rowsCol[i].idd;
                                else if (this.rowsBuffer[1][i])
                                   ar[ar.length]=this.rowsBuffer[0][i];

							return ar.join(separator||",")
						}
dhtmlXGridObject.prototype.getAllItemIds = function(){
	return this.getAllRowIds();
}
   /**
   *   @desc: deletes row specified by ID
   *   @param: row_id - id of row to delete
   *   @param: node - reserved   
   *   @type: public
   *   @topic: 2,9
   */
dhtmlXGridObject.prototype.deleteRow = function(row_id,node){
                                
                        if (!node)node = this.getRowById(row_id)
                        if (!node) return;
                                
                        this.editStop();
                        if (this.callEvent("onBeforeRowDeleted",[row_id])==false)
                           return false;

                    
						if (this.cellType._dhx_find("tree")!=-1)
                        	this._removeTrGrRow(node);
                        else {
                        	if (node.parentNode)
                            	node.parentNode.removeChild(node);
                                   
                           var ind=this.rowsCol._dhx_find(node);
                           if (ind!=-1)
                           	this.rowsCol._dhx_removeAt(ind);
                                else{
                                	ind = this.rowsBuffer[0]._dhx_find(row_id)
                                 	if(ind>=0){
                                    	this.rowsBuffer[0]._dhx_removeAt(ind)
                                    	this.rowsBuffer[1]._dhx_removeAt(ind)
	                                 	}
                				}
                    		this.rowsAr[row_id] = null;
    					}
                    
                    

                            for (var i=0; i<this.selectedRows.length; i++)
                                if (this.selectedRows[i].idd==row_id)
                                    this.selectedRows._dhx_removeAt(i);

                       
                            if(this.pagingOn){
                        this.changePage();
                     }
                     this.setSizes();
                     this.callEvent("onGridReconstructed",[]);
                     if (this._dload) this._askRealRows();
                     return true;
                  }

//#__pro_feature:21092006{
//#colspan:20092006{

/**
*   @desc: dynamicaly set colspan in row starting from specified column index
*   @param: row_id - row id
*   @param: col_id - index of column
*   @param: colspan - size of colspan
*   @type: public
*   @edition: Professional
*   @topic: 2,9
*/
dhtmlXGridObject.prototype.setColspan = function(row_id,col_ind,colspan){
    if (!this._ecspn) return;

    var r=this.getRowById(row_id);
    if ((r._childIndexes)&&(r.childNodes[r._childIndexes[col_ind]])){
        var j=r._childIndexes[col_ind];
        var n=r.childNodes[j];
        var m=n.colSpan;        n.colSpan=1;
        if ((m)&&(m!=1))
            for (var i=1; i<m; i++){
                var c=document.createElement("TD");
                if (n.nextSibling) r.insertBefore(c,n.nextSibling);
                else r.appendChild(c);
                r._childIndexes[col_ind+i]=j+i;
                c._cellIndex=col_ind+i;
                c.align = this.cellAlign[i];
            c.style.verticalAlign = this.cellVAlign[i];
                n=c;
                this.cells3(r,j+i-1).setValue("");
            }

        for (var z=col_ind*1+1*m; z<r._childIndexes.length; z++){
            r._childIndexes[z]+=(m-1)*1;                 }

    }

    if ((colspan)&&(colspan>1)){
        if (r._childIndexes)
            var j=r._childIndexes[col_ind];
        else{
            var j=col_ind;
            r._childIndexes=new Array();
            for (var z=0; z<r.childNodes.length; z++)
                r._childIndexes[z]=z;
            }

        r.childNodes[j].colSpan=colspan;
        for (var z=1; z<colspan; z++){
            r._childIndexes[r.childNodes[j+1]._cellIndex]=j;
            r.removeChild(r.childNodes[j+1]);
        }

        var c1=r.childNodes[r._childIndexes[col_ind]]._cellIndex;
        for (var z=c1*1+1*colspan; z<r._childIndexes.length; z++)
            r._childIndexes[z]-=(colspan-1);

    }
}

//#}
//#}

/**
*   @desc: prevent caching in IE  by adding random values to URL string
*   @param: mode - enable/disable random values in URLs ( disabled by default )
*   @type: public
*   @topic: 2,9
*/
dhtmlXGridObject.prototype.preventIECaching=function(mode){
   this.no_cashe = convertStringToBoolean(mode);
   this.xmlLoader.rSeed=this.no_cashe;
}
dhtmlXGridObject.prototype.preventIECashing=dhtmlXGridObject.prototype.preventIECaching;


/**
*   @desc: enable/disable autosize of column (column size set depending on content size) on doubleclick
*   @param: mode - true/false
*   @type:  public
*/
dhtmlXGridObject.prototype.enableColumnAutoSize = function(mode){
   this._eCAS=convertStringToBoolean(mode);
}
/**
*   @desc: called when header was dbllicked
*   @type: private
*   @topic: 1,2
*/
dhtmlXGridObject.prototype._onHeaderDblClick = function(e){
    var that=this.grid;
     var el = that.getFirstParentOfType(_isIE?event.srcElement:e.target,"TD");

   if (!that._eCAS) return false;
   that.adjustColumnSize(el._cellIndexS)
}

/**
*   @desc: autosize column  to max content size
*   @param: cInd - index of column
*   @type:  public
*/
dhtmlXGridObject.prototype.adjustColumnSize = function(cInd,complex){
   this._notresize=true;
   var m=0;
   this._setColumnSizeR(cInd,20);
   
   for (var j=1; j<this.hdr.rows.length; j++){
         var a=this.hdr.rows[j];
      a=a.childNodes[(a._childIndexes)?a._childIndexes[cInd]:cInd];

      if ((a)&&((!a.colSpan)||(a.colSpan<2))){
         if ((a.childNodes[0])&&(a.childNodes[0].className=="hdrcell"))   a=a.childNodes[0];
         m=Math.max(m,((_isFF||_isOpera)?(a.textContent.length*7):a.scrollWidth));
	  }
   }
	

   var l=this.obj._rowslength();
   for (var i=0; i<l; i++){
	   var z=this.obj._rows(i);
	   if (z._childIndexes && z._childIndexes[cInd]!=cInd) continue;
      if (_isFF||_isOpera||complex)
         z=z.childNodes[cInd].textContent.length*7;
      else
         z=z.childNodes[cInd].scrollWidth;
      if (z>m) m=z;
   }
   m+=20+(complex||0);

   
   this._setColumnSizeR(cInd,m);
   this._notresize=false;
   this.setSizes();
}



/**
*   @desc: remove header line from grid (opposite to attachHeader)
*   @param: index - index of row to be removed ( zero based )
*	@param: hdr - header object (optional)
*   @type:  public
*/
dhtmlXGridObject.prototype.detachHeader = function(index,hdr){
	hdr=hdr||this.hdr;
	var row=hdr.rows[index+1];
	if (row) row.parentNode.removeChild(row);
	this.setSizes();
}

/**
*   @desc: remove footer line from grid (opposite to attachFooter)
*   @param: values - array of header titles
*   @type:  public
*/
dhtmlXGridObject.prototype.detachFooter = function(index){
	this.detachHeader(index,this.ftr);
}

/**
*   @desc: attach additional line to header
*   @param: values - array of header titles
*   @param: style - array of styles, optional
*	@param: _type - reserved
*   @type:  public
*/
dhtmlXGridObject.prototype.attachHeader = function(values,style,_type){
   if (typeof(values)=="string") values=this._eSplit(values);
   if (typeof(style)=="string") style=style.split(this.delim);
   _type=_type||"_aHead";
   if (this.hdr.rows.length){
      if (values)
         this._createHRow([values,style],this[(_type=="_aHead")?"hdr":"ftr"]);
       else if (this[_type])
         for (var i=0; i<this[_type].length; i++)
            this.attachHeader.apply(this,this[_type][i]);
   }
   else{
      if (!this[_type]) this[_type]=new Array();
      this[_type][this[_type].length]=[values,style,_type];
   }
}
/**
*	@desc:
*	@type: private
*/
dhtmlXGridObject.prototype._createHRow = function(data,parent){
   if (!parent){
      //create footer zone
      this.entBox.style.position = "relative";
      var z=document.createElement("DIV");
         z.className="c_ftr".substr(2);
      this.entBox.appendChild(z);
      var t=document.createElement("TABLE");
      t.cellPadding=t.cellSpacing=0;
      if (!_isIE){
            t.width="100%";
         t.style.paddingRight="20px";
        }
        t.style.tableLayout = "fixed";

      z.appendChild(t);
      t.appendChild(document.createElement("TBODY"));
      this.ftr=parent=t;

        var hdrRow =t.insertRow(0);
      var thl=((this.hdrLabels.length<=1)?data[0].length:this.hdrLabels.length);
        for(var i=0;i<thl;i++){
           hdrRow.appendChild(document.createElement("TH"));
           hdrRow.childNodes[i]._cellIndex=i;
        }

        if (_isIE) hdrRow.style.position="absolute";
        else hdrRow.style.height='auto';

   }
   var st1=data[1];
   var z=document.createElement("TR");
    parent.rows[0].parentNode.appendChild(z);
   for (var i=0; i<data[0].length; i++){
      if (data[0][i]=="#cspan"){
         var pz=z.cells[z.cells.length-1];
         pz.colSpan=(pz.colSpan||1)+1;
       continue;
      }
      if ((data[0][i]=="#rspan")&&(parent.rows.length>1)){
         var pind=parent.rows.length-2;
         var found=false;
         var pz=null;
         while(!found){
            var pz=parent.rows[pind];
            for (var j=0; j<pz.cells.length; j++)
               if (pz.cells[j]._cellIndex==i) {
                  found=j+1;
                  break;
            }
            pind--;
         }

         pz=pz.cells[found-1];
         pz.rowSpan=(pz.rowSpan||1)+1;
         continue;
//            data[0][i]="";
      }

      var w=document.createElement("TD");
      w._cellIndex=w._cellIndexS=i;
     if (this.forceDivInHeader)
          w.innerHTML="<div class='hdrcell'>"+data[0][i]+"</div>";
     else
         w.innerHTML=data[0][i];
	if ((data[0][i]||"").indexOf("#")!=-1){
  		var t=data[0][i].match(/(^|{)#([^}]+)(}|$)/);
  		if (t){
  			var tn="_in_header_"+t[2];
  			if (this[tn]) this[tn]((this.forceDivInHeader?w.firstChild:w),i,data[0][i].split(t[0]));
  		}
  	}


	  	
      if (st1) w.style.cssText = st1[i];

      z.appendChild(w);
   }
   var self=parent;
   if (_isKHTML){
         if (parent._kTimer) window.clearTimeout(parent._kTimer);
         parent._kTimer=window.setTimeout(function(){
         parent.rows[1].style.display='none';
         window.setTimeout(function(){ parent.rows[1].style.display=''; },1);
      },500);
   }
}

//#__pro_feature:21092006{
/**
*   @desc: attach additional line to footer
*   @param: values - array of header titles
*   @param: style - array of styles, optional
*   @edition: Professional
*   @type:  public
*/
dhtmlXGridObject.prototype.attachFooter = function(values,style){
   this.attachHeader(values,style,"_aFoot");
}


/**
*   @desc: set excell type for cell in question
*   @param: rowId - row ID
*   @param: cellIndex - cell index
*   @param: type - type of excell (code like "ed", "txt", "ch" etc.)
*   @edition: Professional
*   @type:  public
*/
dhtmlXGridObject.prototype.setCellExcellType = function(rowId,cellIndex,type){
   this.changeCellType(this.rowsAr[rowId],cellIndex,type);
}
/**
*	@desc: 
*	@type: private
*/
dhtmlXGridObject.prototype.changeCellType=function(r,ind,type){
   type=type||this.cellType[ind];
   var z=this.cells3(r,ind);
   var v=z.getValue();
   z.cell._cellType=type;
   var z=this.cells3(r,ind);
   z.setValue(v);
}
/**
*   @desc: set excell type for all cells in specified row
*   @param: rowId - row ID
*   @param: type - type of excell
*   @edition: Professional
*   @type:  public
*/
dhtmlXGridObject.prototype.setRowExcellType = function(rowId,type){
   var z=this.rowsAr[rowId];
   for (var i=0; i<z.childNodes.length; i++)
      this.changeCellType(z,i,type);
}
/**
*   @desc: set excell type for all cells in specified column
*   @param: colIndex - column index
*   @param: type - type of excell
*   @edition: Professional
*   @type:  public
*/
dhtmlXGridObject.prototype.setColumnExcellType = function(colIndex,type){
   for (var i=0; i<this.rowsCol.length; i++)
      this.changeCellType(this.rowsCol[i],colIndex,type);
}

/**
*   @desc: find cell in grid by value
*   @param: value - search string
*   @param: c_ind - index of column to search in (optional. if not specified, then search everywhere)
*   @param: incBufferFl - make search in all rows including buffer (this will parse entire grid and can take time)
*   @edition: Professional
*   @returns: array each member of which contains array with row index and cell index
*   @type:  public
*/
dhtmlXGridObject.prototype.findCell = function(value,c_ind,incBufferFl){
   var res=new Array();
   value=value.toString().toLowerCase();

   if (!this.rowsCol.length) return res;
    for (var i=(c_ind||0); i<this.cellType.length; i++){
       var z=this.cells2(0,i);
      
      if (this.isTreeGrid())
      this.forEachRow(function(id){
         z.cell=this.rowsAr[id].childNodes[i];
         if (!z.cell) return;
         var val=z.getValue();
         if ((val||"").toString().indexOf(value)!=-1) res[res.length]=[id,i];
      });      
      else
  	  for (var j=0; j<this.rowsCol.length; j++){
         z.cell=this.rowsCol[j].childNodes[i];
         if (!z.cell) continue;
         var val=z.getValue();

         if ((val||"").toString().toLowerCase().indexOf(value)!=-1) res[res.length]=[j,i];
		 if(incBufferFl && this.rowsCol.length==j+1) this.addRowsFromBuffer()
      }
      
      if (typeof(c_ind)!="undefined")
         return res;
   }

   return res;
}


//#}
/**
      *   @desc: 
      *   @type: private
      */
dhtmlXGridObject.prototype.dhx_Event=function()
{
   this.dhx_SeverCatcherPath="";

   this.attachEvent = function(original, catcher, CallObj)
   {
      CallObj = CallObj||this;
      original = 'ev_'+original;
       if ( ( !this[original] ) || ( !this[original].addEvent ) ) {
           var z = new this.eventCatcher(CallObj);
           z.addEvent( this[original] );
           this[original] = z;
       }
       return ( original + ':' + this[original].addEvent(catcher) );   //return ID (event name & event ID)
   }
   this.callEvent=function(name,arg0){
         if (this["ev_"+name]) return this["ev_"+name].apply(this,arg0);
       return true;
   }
   this.checkEvent=function(name){
         if (this["ev_"+name]) return true;
       return false;
   }

   this.eventCatcher = function(obj)
   {
       var dhx_catch = new Array();
       var m_obj = obj;
       var func_server = function(catcher,rpc)
                         {
                           catcher = catcher.split(":");
                     var postVar="";
                     var postVar2="";
                           var target=catcher[1];
                     if (catcher[1]=="rpc"){
                           postVar='<?xml version="1.0"?><methodCall><methodName>'+catcher[2]+'</methodName><params>';
                        postVar2="</params></methodCall>";
                        target=rpc;
                     }
                           var z = function() {
                                   }
                           return z;
                         }
       var z = function()
             {
                   if (dhx_catch)
                      var res=true;
                   for (var i=0; i<dhx_catch.length; i++) {
                      if (dhx_catch[i] != null) {
                           var zr = dhx_catch[i].apply( m_obj, arguments );
                           res = res && zr;
                      }
                   }
                   return res;
                }
       z.addEvent = function(ev)
                {
                       if ( typeof(ev) != "function" )
                           if (ev && ev.indexOf && ev.indexOf("server:") == 0)
                               ev = new func_server(ev,m_obj.rpcServer);
                           else
                               ev = eval(ev);
                       if (ev)
                           return dhx_catch.push( ev ) - 1;
                       return false;
                }
       z.removeEvent = function(id)
                   {
                     dhx_catch[id] = null;
                   }
       return z;
   }

   this.detachEvent = function(id)
   {
      if (id != false) {
         var list = id.split(':');            //get EventName and ID
         this[ list[0] ].removeEvent( list[1] );   //remove event
      }
   }
}
/**
*   @desc: execute code for each row in a grid
*   @param: custom_code - function which get row id as incomming argument
*   @type:  public
*/
dhtmlXGridObject.prototype.forEachRow=function(custom_code)
{
   for (a in this.rowsAr)
      if (this.rowsAr[a] && this.rowsAr[a].tagName) custom_code.apply(this,[this.rowsAr[a].idd]);
}
/**
*   @desc: execute code for each cell in a row
*   @param: rowId - id of row where cell must be itterated
*   @param: custom_code - function which get eXcell object as incomming argument
*   @type:  public
*/
dhtmlXGridObject.prototype.forEachCell=function(rowId,custom_code)
{
   var z=this.rowsAr[rowId];
   if (!z) return;
   for (var i=0; i<this._cCount; i++)
        custom_code(this.cells3(z,i));
}
/**
*   @desc: changes grid's container size on the fly to fit total width of grid columns
*   @param: mode  - truse/false - enable / disable
*   @param: max_limit  - max allowed width, not limited by default
*   @param: min_limit  - min allowed width, not limited by default
*   @type:  public
*/
dhtmlXGridObject.prototype.enableAutoWidth = function (mode, max_limit, min_limit){
	this._awdth=[convertStringToBoolean(mode),(max_limit||99999),(min_limit||0)];
 }
 
/**
*   @desc: return unique for current grid id
*   @type:  public
*/
dhtmlXGridObject.prototype.getUID = function (){
	var z=this.getRowsNum()+1;
	while(this.rowsAr[z]) z++;
	return z;
 }
 
 /**
*     @desc: set function called after key pressed in grid
*     @param: func - event handling function
*     @type: depricated
*     @edition: Professional
*     @topic: 10
*     @event:  onKeyPress
*     @eventdesc: event fired after key pressed but before default key processing started
*     @eventparam: key code
*     @eventparam: control key flag
*     @eventparam: shift key flag
*     @eventreturns: false - block defaul key processing
*/
   dhtmlXGridObject.prototype.setOnKeyPressed=function(func){
                this.attachEvent("onKeyPress",func);
    };
 
/**
*   @desc: refresh grid from XML ( doesnt work for buffering, tree grid or rows in smart rendering mode )
*   @param: insert_new - insert new items
*   @param: del_missed - delete missed rows
*   @param: afterCall - function, will be executed after refresh completted
*   @type:  public
*/

dhtmlXGridObject.prototype.updateFromXML=function(url,insert_new,del_missed,afterCall)
{
	if (typeof insert_new == "undefined")
		insert_new=true;
	this._refresh_mode=[true,insert_new,del_missed];
	if (afterCall) this.xmlLoader.waitCall=afterCall;
	this.callEvent("onXLS",[this]);
	this.xmlLoader.loadXML(url);
}
dhtmlXGridObject.prototype.updateFromXMl=dhtmlXGridObject.prototype.updateFromXML;
/**
      *   @desc: 
      *   @type: private
      */
dhtmlXGridObject.prototype._refreshFromXML=function(xml)
{
      if (window.eXcell_tree){
	  	eXcell_tree.prototype.setValueX=eXcell_tree.prototype.setValue;
	  	eXcell_tree.prototype.setValue=function(content){ 
    		if (this.grid._h2.get[this.cell.parentNode.idd]){
	    		this.setLabel(content[1]);
	    		if (content[3]) this.setImage(content[3]);
	    	}
	    	else
    			this.setValueX(content);
			};
	  }

	var tree=this.cellType._dhx_find("tree");
    var pid=xml.doXPath("//rows")[0].getAttribute("parent")||0;
    
	var del={};
	if (this._refresh_mode[2]){
		this.forEachRow(function(id){
			del[id]=true;				
		});}
		
	var rows=xml.doXPath("//row");
	for (var i=0; i<rows.length; i++){
		var row=rows[i];
		var id=row.getAttribute("id");
		del[id]=false;
		
		if (this._dload || this.rowsBuffer[0].length){
			if (this.rowsAr[id])
				this._fillRowFromXML(this.rowsAr[id],row,-1);
			else{
					var z=this.rowsBuffer[0]._dhx_find(id);
					if (z!=-1) 
						this.rowsBuffer[1][z]=row;
				}
		}
		else
		if (this.rowsAr[id])
			this._fillRowFromXML(this.rowsAr[id],row,tree,pid);
		else if(this._refresh_mode[1]){
			var r=this._prepareRow(id);
                r=this._fillRowFromXML(r,row,tree,pid);
                if (tree!=-1 && this._h2.get[pid].state=="minus")
                	r = this._insertRowAt(r,this.getRowIndex(pid)+this._getOpenLenght(pid,0));
                else
                	r = this._insertRowAt(r);
                this._postRowProcessing(r,row)
		}
	}
	
	if (this._refresh_mode[2])
		for (id in del){
			if (del[id] && this.rowsAr[id])
				this.deleteRow(id);
		}

      if (window.eXcell_tree)
	  	eXcell_tree.prototype.setValue=eXcell_tree.prototype.setValueX;
	this.callEvent("onXLE",[this,rows.length]);
}


/**
*   @desc: get combobox specific for cell in question
*   @param: id - row id
*   @param: ind  - row index
*   @type:  public
*/
dhtmlXGridObject.prototype.getCustomCombo=function(id,ind){
	var cell= this.cells(id,ind).cell;
	if (!cell._combo)
		cell._combo = new dhtmlXGridComboObject();
	return cell._combo;
}
/**
*   @desc: set tab order of columns
*   @param: order - list of tab indexes (default delimiter is ",")
*   @type:  public
*/
dhtmlXGridObject.prototype.setTabOrder=function(order){
	var t=order.split(this.delim);
	this._tabOrder=[];
	for (var i=0; i < this._cCount; i++) 
		t[i]={c:parseInt(t[i]), ind:i};
	t.sort(function(a,b){  return (a.c>b.c?1:-1); });
	for (var i=0; i < this._cCount; i++) 
		if (!t[i+1] || (typeof t[i].c == "undefined"))
			this._tabOrder[t[i].ind]=(t[0].ind+1)*-1;
		else
			this._tabOrder[t[i].ind]=t[i+1].ind;
}
dhtmlXGridObject.prototype.i18n={
	loading:"Loading"
}
//key_ctrl_shift
dhtmlXGridObject.prototype._key_events={
			k13_1_0:function(){
				var rowInd = this.rowsCol._dhx_find(this.row)
                this.selectCell(this.rowsCol[rowInd+1],this.cell._cellIndex,true);
			},
			k13_0_1:function(){
				var rowInd = this.rowsCol._dhx_find(this.row)
                this.selectCell(this.rowsCol[rowInd-1],this.cell._cellIndex,true);
			},
			k13_0_0:function(){
				this.editStop();
            	this.callEvent("onEnter",[(this.row?this.row.idd:null),(this.cell?this.cell._cellIndex:null)]);
            },
            k9_0_0:function(){
				this.editStop();
				var z=this._getNextCell(null,1);
				if (z) {
					this.selectCell(z.parentNode,z._cellIndex,(this.row!=z.parentNode),false,true);
					this._still_active=true;
				}
            },
			k9_0_1:function(){
				this.editStop();
				var z=this._getNextCell(null,-1);
				if (z) {
					this.selectCell(z.parentNode,z._cellIndex,(this.row!=z.parentNode),false,true);
					this._still_active=true;
				}
            },
            k113_0_0:function(){
            	if (this._f2kE) this.editCell();
            },
            k32_0_0:function(){
            	var c=this.cells4(this.cell);
            	if (!c.changeState || (c.changeState()===false)) return false;
            },
            k27_0_0:function(){
            	this.editStop(true);
            },
            k33_0_0:function(){
            	if(this.pagingOn)
            		this.changePage(this.currentPage-1);
            	else this.scrollPage(-1);            		
	        },
			k34_0_0:function(){
            	if(this.pagingOn)
            		this.changePage(this.currentPage+1);
            	else this.scrollPage(1);
	        },
			k37_0_0:function(){
            	if(!this.editor && this.isTreeGrid())
            		this.collapseKids(this.row)
            	else return false;
	        },
			k39_0_0:function(){
				if(!this.editor && this.isTreeGrid())
            		this.expandKids(this.row)
            	else return false;
            },
			k40_0_0:function(){
				if (this.editor && this.editor.combo)
					this.editor.shiftNext();
				else{
					var rowInd = this.rowsCol._dhx_find(this.row)+1;
					if (rowInd!=this.rowsCol.length && rowInd!=this.obj.rows.length-1){
						var nrow=this._nextRow(rowInd-1,1);
						if (nrow._sRow || nrow._rLoad) return false;
                        this.selectCell(nrow,this.cell._cellIndex,true);
                    }
                    else {
                    	this._key_events.k34_0_0.apply(this,[]);
                    	if (this.pagingOn && this.rowsCol[(this.currentPage-1)*this.rowsBufferOutSize])
                    		this.selectCell((this.currentPage-1)*this.rowsBufferOutSize,0,true);
                    }
				}
            },
			k38_0_0:function(){		
				if (this.editor && this.editor.combo)
					this.editor.shiftPrev();
				else{
					var rowInd = this.rowsCol._dhx_find(this.row)+1;
					if (rowInd!=-1 && (!this.pagingOn || (this.currentPage-1)*this.rowsBufferOutSize+1 < rowInd )){
						var nrow=this._nextRow(rowInd-1,-1);
						if (!nrow || nrow._sRow || nrow._rLoad) return false;
                    	this.selectCell(nrow,this.cell._cellIndex,true);
					}
					else {
						this._key_events.k33_0_0.apply(this,[]);
						if (this.pagingOn && this.rowsCol[this.currentPage*this.rowsBufferOutSize-1])
                    		this.selectCell(this.currentPage*this.rowsBufferOutSize-1,0,true);
	                }
				}
            }
		};
/**
*   @desc: enables/disables mode when readonly cell is not available with tab 
*   @param: mode - (boolean) true/false
*   @type:  public
*/
dhtmlXGridObject.prototype.enableSmartTabOrder = function(mode){
	if(arguments.length > 0) this.smartTabOrder = convertStringToBoolean(mode);
	else this.smartTabOrder = true;
}
/**
*   @desc: sets elements which get focus when tab is pressed in the last or first (tab+shift) cell 
*   @param: start - html object or its id - gets focus when tab+shift are pressed in the first cell  
*   @param: end - html object or its id - gets focus when tab is pressed in the last cell  
*   @type:  public
*/
dhtmlXGridObject.prototype.setExternalTabOrder = function(start,end){
	var grid = this;
	this.tabStart = (typeof(start)=="object")?start: document.getElementById(start);
	this.tabStart.onkeydown = function(e){
		var ev = (e||window.event);
		ev.cancelBubble=true;
		if(ev.keyCode==9){
			grid.selectCell(0,0,0,0,1); 
			if(grid.cells2(0,0).isDisabled()){
				grid._key_events["k9_0_0"].call(grid);
			}
			return false;
		}
		
	}
	
	this.tabEnd = (typeof(end)=="object")?end:document.getElementById(end);
	this.tabEnd.onkeydown = function(e){
		var ev = (e||window.event);
		ev.cancelBubble=true;  
		if((ev.keyCode == 9) && ev.shiftKey){
			grid.selectCell((grid.getRowsNum()-1),(grid.getColumnCount()-1),0,0,1); 
			if(grid.cells2((grid.getRowsNum()-1),(grid.getColumnCount()-1)).isDisabled()){
				grid._key_events["k9_0_1"].call(grid);
			}
			return false;
		}
		
	}
	
}

//(c)dhtmlx ltd. www.dhtmlx.com

