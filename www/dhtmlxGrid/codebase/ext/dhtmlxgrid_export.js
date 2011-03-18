//v.2.6 build 100722

/*
Copyright DHTMLX LTD. http://www.dhtmlx.com
You allowed to use this component or parts of it under GPL terms
To use it on other terms or get Professional edition of the component please contact us at sales@dhtmlx.com
*/
dhtmlXGridObject.prototype.toPDF=function(url,mode,header,footer,rows){mode = mode || "color";var grid = this;grid._asCDATA = true;eXcell_ch.prototype.getContent = function(){return this.getValue();};eXcell_ra.prototype.getContent = function(){return this.getValue();};function xml_top(profile) {var spans = [];for (var i=1;i<grid.hdr.rows.length;i++){spans[i]=[];for (var j=0;j<grid._cCount;j++){var cell = grid.hdr.rows[i].childNodes[j];if (!spans[i][j])spans[i][j]=[0,0];if (cell)spans[i][cell._cellIndexS]=[cell.colSpan, cell.rowSpan];}};var xml = "<rows profile='"+profile+"'";if (header)xml+=" header='"+header+"'";if (footer)xml+=" footer='"+footer+"'";xml+="><head>"+grid._serialiseExportConfig(spans).replace(/^<head/,"<columns").replace(/head>$/,"columns>");for (var i=2;i < grid.hdr.rows.length;i++){var empty_cols = 0;var row = grid.hdr.rows[i];var cxml="";for (var j=0;j < grid._cCount;j++){var s = spans[i][j];var rspan = (( s[0] && s[0] > 1 ) ? ' colspan="'+s[0]+'" ' : "");if (s[1] && s[1] > 1){rspan+=' rowspan="'+s[1]+'" ';empty_cols = -1;};var val = "";for (var k=0;k<row.cells.length;k++){if (row.cells[k]._cellIndexS==j){if (row.cells[k].getElementsByTagName("SELECT").length)
 val="";else
 val = _isIE?row.cells[k].innerText:row.cells[k].textContent;val=val.replace(/[ \n\r\t\xA0]+/," ");break;}};if (!val || val==" ")empty_cols++;cxml+="<column"+rspan+"><![CDATA["+val+"]]></column>";};if (empty_cols != grid._cCount)xml+="\n<columns>"+cxml+"</columns>";};xml+="</head>\n";return xml;};function xml_body() {var xml =[];if (rows)for (var i=0;i<rows.length;i++)xml.push(xml_row(grid.getRowIndex(rows[i])));else
 for (var i=0;i<grid.getRowsNum();i++)
 xml.push(xml_row(i));return xml.join("\n");};function xml_row(ind){if (!grid.rowsBuffer[ind])return "";var r = grid.render_row(ind);if (r.style.display=="none")return "";var xml = "<row>";for (var i=0;i < grid._cCount;i++){if ((!this._srClmn)||(this._srClmn[i])){var cell = grid.cells(r.idd, i);xml+="<cell><![CDATA["+(cell.getContent?cell.getContent():cell.getTitle())+"]]></cell>";}};return xml+"</row>";};function xml_end(){var xml = "</rows>";return xml;};var d=document.createElement("div");d.style.display="none";document.body.appendChild(d);var uid = "form_"+grid.uid();d.innerHTML = '<form id="'+uid+'" method="post" target="_blank" action="'+url+'" accept-charset="utf-8"><input type="hidden" name="grid_xml" id="grid_xml"/> </form>';document.getElementById(uid).firstChild.value = xml_top(mode).replace("\u2013", "-") + xml_body() + xml_end();document.getElementById(uid).submit();d.parentNode.removeChild(d);grid = null;};dhtmlXGridObject.prototype._serialiseExportConfig=function(spans){var out = "<head>";for (var i = 0;i < this.hdr.rows[0].cells.length;i++){if (this._srClmn && !this._srClmn[i])continue;var sort = this.fldSort[i];if (sort == "cus"){sort = this._customSorts[i].toString();sort=sort.replace(/function[\ ]*/,"").replace(/\([^\f]*/,"");};var s = spans[1][i];var rpans = (( s[1] && s[1] > 1 ) ? ' rowspan="'+s[1]+'" ' : "")+(( s[0] && s[0] > 1 ) ? ' colspan="'+s[0]+'" ' : "");out+="<column "+rpans+" width='"+this.getColWidth(i)+"' align='"+this.cellAlign[i]+"' type='"+this.cellType[i]
 +"' sort='"+(sort||"na")+"' color='"+(this.columnColor[i]||"")+"'"
 +(this.columnIds[i]
 ? (" id='"+this.columnIds[i]+"'")
 : "")+">";if (this._asCDATA)out+="<![CDATA["+this.getHeaderCol(i)+"]]>";else
 out+=this.getHeaderCol(i);var z = this.getCombo(i);if (z)for (var j = 0;j < z.keys.length;j++)out+="<option value='"+z.keys[j]+"'>"+z.values[j]+"</option>";out+="</column>";};return out+="</head>";};dhtmlXGridObject.prototype.toExcel = dhtmlXGridObject.prototype.toPDF;

//v.2.6 build 100722

/*
Copyright DHTMLX LTD. http://www.dhtmlx.com
You allowed to use this component or parts of it under GPL terms
To use it on other terms or get Professional edition of the component please contact us at sales@dhtmlx.com
*/