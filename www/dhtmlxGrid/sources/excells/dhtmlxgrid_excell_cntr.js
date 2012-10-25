//v.2.6 build 100722

/*
Copyright DHTMLX LTD. http://www.dhtmlx.com
You allowed to use this component or parts of it under GPL terms
To use it on other terms or get Professional edition of the component please contact us at sales@dhtmlx.com
*/
/*
Counter eXcell v.1.0  for dhtmlxGrid 
(c)DHTMLX LTD. 2005


The corresponding  cell value in XML can contain any value (it is ignored)

*/
/**
*	@desc: auto counter editor
*	@returns: dhtmlxGrid cell editor object
*	@type: public
*/
function eXcell_cntr(cell){
	this.cell = cell;
    this.grid = this.cell.parentNode.grid;
	if (!this.grid._ex_cntr_ready && !this._realfake){
		this.grid._ex_cntr_ready=true;
		if (this.grid._h2)
			this.grid.attachEvent("onOpenEn",function(id){
				this.resetCounter(cell._cellIndex);
			});
		this.grid.attachEvent("onBeforeSorting",function(){ 
			var that=this;
			window.setTimeout(function(){ 
				if (that._fake && !that._realfake && cell._cellIndex<that._fake._cCount) 
					that._fake.resetCounter(cell._cellIndex); 
				else
				    that.resetCounter(cell._cellIndex);
			},1)
			return true;
		});
	}
	
	

	this.edit = function(){}
	this.getValue = function(){
		return this.cell.innerHTML;
	}
	this.setValue = function(val){
		this.cell.style.paddingRight = "2px";
		var cell=this.cell;
		
		window.setTimeout(function(){
			if (!cell.parentNode) return;
			var val=cell.parentNode.rowIndex;
			if (cell.parentNode.grid.currentPage || val<0 || cell.parentNode.grid._srnd) val=cell.parentNode.grid.rowsBuffer._dhx_find(cell.parentNode)+1;
			if (val<=0) return;
			cell.innerHTML = val;
			if (cell.parentNode.grid._fake && cell._cellIndex<cell.parentNode.grid._fake._cCount && cell.parentNode.grid._fake.rowsAr[cell.parentNode.idd]) cell.parentNode.grid._fake.cells(cell.parentNode.idd,cell._cellIndex).setCValue(val);
			cell=null;
		},100);
	}
}
dhtmlXGridObject.prototype.resetCounter=function(ind){
	if (this._fake && !this._realfake && ind < this._fake._cCount) this._fake.resetCounter(ind,this.currentPage);
	var i=arguments[0]||0;
	if (this.currentPage)
		i=(this.currentPage-1)*this.rowsBufferOutSize;
	for (i=0; i<this.rowsBuffer.length; i++)
		if (this.rowsBuffer[i].tagName == "TR")
			this.rowsAr[this.rowsBuffer[i].idd].childNodes[ind].innerHTML=i+1;
}
eXcell_cntr.prototype = new eXcell;
//(c)dhtmlx ltd. www.dhtmlx.com
