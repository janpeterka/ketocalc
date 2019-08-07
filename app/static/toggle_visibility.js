function toggleVisibility() {
   const x = $('#password');
    if (x.attr("type") === "password") {
        x.attr("type", 'text');
    } else {
        x.attr("type", 'password');
    }
}

function turnOnVisibility() {
	const x = $('#password');
   	x.attr("type", 'text');
}

function turnOffVisibility() {
	const x = $('#password');
   	x.attr("type", 'password');
}
