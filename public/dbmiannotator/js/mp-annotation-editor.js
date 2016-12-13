// MP CLAIM ================================================================================
// open claim editor
function claimEditorLoad() {
    currFormType = "claim";
    $("#mp-claim-form").show();
    $('#quote').show();
    $("#claim-label-data-editor").hide();
    $(".annotator-save").hide();
    $("#mp-data-nav").hide();
    $("#mp-data-form-evRelationship").hide();
    $("#mp-data-form-participants").hide();
    $("#mp-data-form-dose1").hide();
    $("#mp-data-form-dose2").hide();
    $("#mp-data-form-phenotype").hide();
    $("#mp-data-form-auc").hide();
    $("#mp-data-form-cmax").hide();
    $("#mp-data-form-clearance").hide();
    $("#mp-data-form-halflife").hide();
    $("#mp-data-form-studytype").hide();
}


// edit claim
function editClaim() {
    annotationId = $('#mp-editor-claim-list option:selected').val();

    scrollToAnnotation(annotationId, "claim", 0);
    showEditor();
    claimEditorLoad();
        
    $.ajax({url: "http://" + config.annotator.host + "/annotatorstore/annotations/" + annotationId,
            data: {},
            method: 'GET',
            error : function(jqXHR, exception){
                console.log(exception);
            },
            success : function(annotation){
                // enable delete button
                $("#annotator-delete").show();
                
                // call AnnotatorJs editor for update    
                app.annotations.update(annotation);   
            }
           });        
}


$("#Drug1").change(function (){selectDrug();});
$("#Drug2").change(function (){selectDrug();});

function selectDrug() {
    var drug1 = $("#Drug1").val();
    var drug2 = $("#Drug2").val();
    var quotestring = $("#quote").html();
    quotestring = quotestring.replace(drug2, "<span class='selecteddrug'>"+drug2+"</span>");
    quotestring = quotestring.replace(drug1, "<span class='selecteddrug'>"+drug1+"</span>");
    $("#quote").html(quotestring);
}

$("#Drug1").mousedown(function (){deselectDrug();});
$("#Drug2").mousedown(function (){deselectDrug();});

function deselectDrug() {
    var drug1 = $("#Drug1").val();
    var drug2 = $("#Drug2").val();
    var quotestring = $("#quote").html();
    quotestring = quotestring.replace("<span class='selecteddrug'>"+drug2+"</span>", drug2);
    quotestring = quotestring.replace("<span class='selecteddrug'>"+drug1+"</span>", drug1);
    $("#quote").html(quotestring);
}

// when method is phenotype and relationship is inhibits or substrate of
function changeCausedbyMethod() {
    var methodValue = $("#method option:selected").text();
    //statement
    if (methodValue == "statement") {
        $('#negationdiv').show();
        $('#negation-label').show();
    } else {
        $('#negationdiv').hide();
        $('#negation-label').hide();
    }
    //phenotype - no interact with
    if (methodValue == "Phenotype clinical study") {
        $("#relationship option[value = 'interact with']").attr('disabled', 'disabled');
        $("#relationship option[value = 'interact with']").hide();

        if ($("#relationship option:selected").text() == "interact with") {
            $("#relationship option:selected").prop("selected", false);
        }
    } else {
        $("#relationship option[value = 'interact with']").removeAttr('disabled');
        $("#relationship option[value = 'interact with']").show();
    }
    //case report - no substrate of or inhibits
    if (methodValue == "Case Report") {
        $("#relationship option[value = 'inhibits']").attr('disabled', 'disabled');
        $("#relationship option[value = 'inhibits']").hide();
        $("#relationship option[value = 'substrate of']").attr('disabled', 'disabled');
        $("#relationship option[value = 'substrate of']").hide();
        if ($("#relationship option:selected").text() == "inhibits" || $("#relationship option:selected").text() == "substrate of") {
            $("#relationship option:selected").prop("selected", false);
        }
    } else {
        $("#relationship option[value = 'inhibits']").removeAttr('disabled');
        $("#relationship option[value = 'inhibits']").show();
        $("#relationship option[value = 'substrate of']").removeAttr('disabled');
        $("#relationship option[value = 'substrate of']").show();
    }
    //phenotype & statement
    if ((methodValue == "Phenotype clinical study" || methodValue == "statement") && ($("#relationship option:selected").text() == "inhibits"||$("#relationship option:selected").text()=="substrate of")) {
        $("#Drug1-label").html("Drug: ");
        $("#Drug2-label").parent().hide();
        $("#Drug2").parent().hide();
        $("#enzymesection1").show();
        $("#enzyme").show();

        $('input[name=precipitant]').prop('checked', false);
        $('input[type=radio][name=precipitant]').parent().hide();
        $('.precipitantLabel').parent().hide();
    } else {
        $("#Drug1-label").html("Drug1: ");
        $("#Drug2-label").parent().show();
        $("#Drug2").parent().show();
        $("#Drug2")[0].selectedIndex = 0;
        console.log($("#Drug2 option:selected").text());
    }
}

// when type is Genotype
function showPhenotypeType() {
    console.log($("input[name=phenotypeGenre]:checked").val());
    console.log($("input[name=phenotypeMetabolizer]:checked").val());
    if ($("input:radio[name=phenotypeGenre]:checked").val() == "Genotype") {
        $('#geneFamily').show();
        $('#geneFamily-label').show();
        $('#markerDrug').hide();
        $('#markerDrug-label').hide();
    } else {
        $('#geneFamily').hide();
        $('#geneFamily-label').hide();
        $('#markerDrug').show();
        $('#markerDrug-label').show();
    }
}

// when relationship is inhibits or substrate of, show field enzyme
function showEnzyme() {

    if($("#relationship option:selected").text() == "inhibits"||$("#relationship option:selected").text()=="substrate of") {
        if ($("#method option:selected").text() == "Phenotype clinical study" || $("#method option:selected").text() == "statement") {
            $("#Drug1-label").html("Drug: ");
            $("#Drug2-label").parent().hide();
            $("#Drug2").parent().hide();
        } else {
            $("#Drug1-label").html("Drug1: ");
            $("#Drug2-label").parent().show();
            $("#Drug2").parent().show();
        }
        $("#enzyme")[0].selectedIndex = 0;
        $("#enzymesection1").show();
        $("#enzyme").show();

        $('input[name=precipitant]').prop('checked', false);
        $('input[type=radio][name=precipitant]').parent().hide();
        $('.precipitantLabel').parent().hide();
    }
    if($("#relationship option:selected").text()=="interact with") {
        $("#Drug1-label").html("Drug1: ");
        $("#Drug2-label").parent().show();
        $("#Drug2").parent().show();
        $("#enzymesection1").hide();
        $("#enzyme").hide();
        $('input[type=radio][name=precipitant]').parent().show();
        $('.precipitantLabel').parent().show();
    }
}


// modify annotaiton id when user pick claim on mpadder's menu
// update annotation table if necessary
function claimSelectedInMenu(annotationId) {
    currAnnotationId = annotationId;
    annTableId = $('#mp-editor-claim-list option:selected').val();

    if (annotationId != annTableId){
        $("#mp-editor-claim-list option[value='" + annotationId + "']").attr("selected", "true");
        changeClaimInAnnoTable();
    }
}

// MP DATA & MATERIAL ========================================================================
// called when click annotation table cell when value of cell is empty
// (1) if no text selection avaliable, then pop up warning message then return 
// to mp annotation table
// (2) otherwise, load annotation to editor, then shown specific data form
function addDataCellByEditor(field, dataNum, isNewData) {

    $("#button#drug1-dose-switch-btn").focus();

    var annotationId = $('#mp-editor-claim-list option:selected').val();
    console.log("addDataCellByEditor - id: " + annotationId + " | data: " + dataNum + " | field: " + field);

    $("#claim-label-data-editor").show();
    //fields whitch don't need text selected
    var selectedTextNotNeed = ["evRelationship", "studytype", "reviewer", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"];

    // return if no text selection 
    if (!isTextSelected && !selectedTextNotNeed.includes(field)) {
        warnSelectTextSpan(field);
    } else {
        // hide data fields navigation if editing evidence relationship 
        if (field == "evRelationship" || field == "studytype") {
            $("#mp-data-nav").hide();
            $(".annotator-save").hide();
        } else {
            $(".annotator-save").show();            
        }

        // cached editing data cell
        currAnnotationId = annotationId;
        currDataNum = dataNum;
        currFormType = field;

        showEditor();
        if (cachedOATarget.hasSelector != null)
            $("#" + field + "quote").html(cachedOATarget.hasSelector.exact);
        $("#annotator-delete").hide();
        
        // updating current MP annotation
        if (annotationId != null)
            currAnnotationId = annotationId;     

        preDataForm(field);

        $.ajax({url: "http://" + config.annotator.host + "/annotatorstore/annotations/" + annotationId,
                data: {},
                method: 'GET',
                error : function(jqXHR, exception){
                    console.log(exception);
                },
                success : function(annotation){
                    // add data if not avaliable  
                    if (annotation.argues.supportsBy.length == 0 || isNewData){ 

                        var data = {type : "mp:data", evRelationship: "", auc : {}, cmax : {}, clearance : {}, halflife : {}, reviewer: {}, dips: {}, supportsBy : {type : "mp:method", supportsBy : {type : "mp:material", participants : {}, drug1Dose : {}, drug2Dose : {}, phenotype: {}}}, grouprandom: "", parallelgroup: ""};
                        annotation.argues.supportsBy.push(data); 
                    } 
                    
                    // call AnnotatorJs editor for update    
                    app.annotations.update(annotation);
  
                }                 
               });
        }
}
              
        
// called when click annotation table cell when value of cell is not null
// (1) scroll to the annotation upon document
// (2) load annotation to editor, then shown specific data form
function editDataCellByEditor(field, dataNum) {

    showEditor();
    $("#claim-label-data-editor").show();
    $('#quote').hide();
    
    // hide data fields navigation if editing evidence relationship 
    if (field == "evRelationship" || field == "studytype") {
        $("#mp-data-nav").hide();
        $(".annotator-save").hide();
    } else {
        $(".annotator-save").show();
    }

    var annotationId = $('#mp-editor-claim-list option:selected').val();
    console.log("editDataCellByEditor - id: " + annotationId + " | data: " + dataNum + " | field: " + field);
    
    // cached editing data cell
    currAnnotationId = annotationId;
    currDataNum = dataNum;
    currFormType = field;

    // scroll to the position of annotation
    scrollToAnnotation(annotationId, field, dataNum);
        
    $.ajax({url: "http://" + config.annotator.host + "/annotatorstore/annotations/" + annotationId,
            data: {},
            method: 'GET',
            error : function(jqXHR, exception){
                console.log(exception);
            },
            success : function(annotation){
                
                // updating current MP annotation
                if (annotationId != null)
                    currAnnotationId = annotationId;
                
                //switchDataForm(field, true);
                preDataForm(field, true);

                // show delete button
                data = annotation.argues.supportsBy[dataNum];
                material = data.supportsBy.supportsBy;
                if ((field == "participants" && material.participants.value != null) || (field == "dose1" && material.drug1Dose.value != null) || (field == "dose2" && material.drug2Dose.value != null) || ((field == "auc" || field == "cmax" || field == "clearance" || field == "halflife") && (data[field].value != null)))
                    $("#annotator-delete").show();
                
                // call AnnotatorJs editor for update    
                app.annotations.update(annotation);   
            }
           });               
}

// warning dialog for opening data editor
function preDataForm(targetField, isNotNeedValid) {
    $("#mp-claim-form").hide();
    quoteF = $('#'+targetField+'quote').html();         
    // unsaved warning box  
    if (!warnUnsavedDialog())
        return;

    if (!isTextSelected && (targetField != "evRelationship" || targetField != "studytype") && quoteF == "" && !isNotNeedValid) {
        warnSelectTextSpan(targetField);
        return;
    } 
    
    if (targetField == null) 
        targetField = "participants";

    currFormType = targetField;

    focusOnDataField(targetField);
}

// switch data from nav button
function switchDataForm(targetField, isNotNeedValid) {

    $("#mp-claim-form").hide();
    quoteF = $('#'+targetField+'quote').html();         
    // unsaved warning box  
    if (!warnUnsavedDialog())
        return;

    // pop up warn for selecting span when switch to new targetField dring editing mode
    if (!isTextSelected && (targetField != "evRelationship" || targetField != "studytype") && quoteF == "" && !isNotNeedValid) {
        warnSelectTextSpan(targetField);
        return;
    } 
    

    if (targetField == null) 
        targetField = "participants";

    currFormType = targetField;

    try {
        
        //redraw data currhighlight & add/edit data to currAnnotation
        app.annotations.update(currAnnotation);
        // scroll to the position of annotation
        scrollToAnnotation(currAnnotation.id, currFormType, currDataNum);
        
        switchDataFormHelper(targetField);

    } catch (err) {
        console.log(err);
    }
}

// when switch data field, show or hide delete button, nav buttons and data forms 
function switchDataFormHelper(targetField) {

    // field actual div id mapping
    fieldM = {"reviewer":"reviewer", "evRelationship":"evRelationship", "participants":"participants", "dose1":"drug1Dose", "dose2":"drug2Dose", "phenotype":"phenotype", "auc":"auc", "cmax":"cmax", "clearance":"clearance", "halflife":"halflife", "studytype":"studytype"};

    var showDeleteBtn = false;
    var questionList = ["reviewer", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"];
    if (questionList.includes(targetField)){
        console.log("show dips editor");
        $("#mp-data-form-"+targetField).show();
    }

    for (var field in fieldM) {       
        var dataid = "mp-data-form-"+field;
        if (field === targetField) {
            $("#"+dataid).show();  // show specific data form 
            // inspect that is target form has value filled 

            if (field == "evRelationship" || field =="studytype") { // when field is radio button
                fieldVal = $("input[name="+field+"]:checked").val();
            } else if (field == "auc" || field == "cmax" || field == "clearance" || field == "halflife") { // when field is checkbox
                $("#mp-data-nav").show();
                if ($('#' + field + '-unchanged-checkbox').is(':checked')) 
                    showDeleteBtn = true;                    
                fieldVal = $("#" + fieldM[field]).val();
            } else { // when field is text input
                $("#mp-data-nav").show();
                fieldVal = $("#" + fieldM[field]).val();
            }

            if (fieldVal !=null && fieldVal != "")
                $("#annotator-delete").show();
            else if (showDeleteBtn)
                $("#annotator-delete").show();
            else 
                $("#annotator-delete").hide();
            focusOnDataField(targetField);
        }  else {
            cleanFocusOnDataField(field);
            $("#"+dataid).hide();
        }                           
    }
}


// scroll current focus on window to specific highlight piece
function scrollToAnnotation(annotationId, fieldName, dataNum) {
    var divId = annotationId + "-" + fieldName + "-" + dataNum;
    if (document.getElementById(divId))
        document.getElementById(divId).scrollIntoView(true);
}

// unselect study type questions 
function clearStudyTypeQuestions() {
    $('input[name=grouprandom]').prop('checked', false);
    $('input[name=parallelgroup]').prop('checked', false);
}


function focusOnDataField (fieldName) {
    $("button#nav-"+fieldName+"-btn").css("border","3px solid #336699");
}


function cleanFocusOnDataField(fieldName) {
    $("button#nav-"+fieldName+"-btn").css("border","");
}
