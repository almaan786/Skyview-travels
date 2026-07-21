function nextStep()
{
    document.getElementById("step1").style.display = "none";
    document.getElementById("step2").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 2 of 4";
}

function previousStep()
{
    document.getElementById("step2").style.display = "none";
    document.getElementById("step1").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 1 of 4";
}

function goToStep3()
{
    document.getElementById("step2").style.display = "none";
    document.getElementById("step3").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 3 of 4";
}

function backToStep2()
{
    document.getElementById("step3").style.display = "none";
    document.getElementById("step2").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 2 of 4";
}

function goToStep4()
{
    document.getElementById("step3").style.display = "none";
    document.getElementById("step4").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 4 of 4";
}

function backToStep3()
{
    document.getElementById("step4").style.display = "none";
    document.getElementById("step3").style.display = "block";

    document.getElementById("stepIndicator").innerHTML = "Step 3 of 4";
}
