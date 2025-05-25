function display(value){
    document.getElementById("input-text").value += value;
}

function clearScreen() {
    document.getElementById("input-text").value = " "
}
// function calculate() {
//     var p = document.getElementById("input-text").value;
//     var q = eval(p)
//     document.getElementById("input-text").value = q;
// }

function calculate() {
    var expression = document.getElementById("input-text").value;
    try {
        var result = eval(expression);
        if (result === Infinity || result === -Infinity) {
            throw new Error("Division by Zero");
        }
        document.getElementById("input-text").value = result;
    } catch (e) {
        document.getElementById("input-text").value = "Error";
    }
}
