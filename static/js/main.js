// change navbar styles on scroll

window.addEventListener('scroll', () => { document.querySelector('nav').classList.toggle('window-scroll', window.scrollY > 0) })

// show/hide faq answer 

const faqs = document.querySelectorAll('.faq');

faqs.forEach(faq => {
    faq.addEventListener('click', () => {
        faq.classList.toggle('open');

        //change icon
        const icon = feq.querySelector('.faq__icon i');
        if (icon.className === 'uil uil-plus') {
            icon.className = "uil uil-minus";
        } else {
            icon.className = "uil uil-plus";
        }
    })
})



//show/hide nav menu

const menu = document.querySelector(".nav__menu");
const menuBtn = document.querySelector("#open-menu-btn");
const closeBtn = document.querySelector("#close-menu-btn");


menuBtn.addEventListener('click', () => {
    menu.style.display = "flex";
    closeBtn.style.display = "inline-block";
    menuBtn.style.display = "none";

})

//close nav menu 
const closeNav = () => {
    menu.style.display = "none";
    closeBtn.style.display = "none";
    menuBtn.style.display = "inline-block";

}

closeBtn.addEventListener('click', closeNav)



// Gallery================Document


// Get the modals
var modal1 = document.getElementById("myModal1");

// Get the button that opens the modal
var btn1 = document.querySelector("button[onclick='openModal()']");

// Get the <span> element that closes the modal
var span1 = document.querySelector("#myModal1 .close");

// When the user clicks the button, open the modal
/* Open modal popup */
function openModal() {
    document.getElementById("myModal1").style.display = "block";
}

/* Close modal popup */
function closeModal() {
    document.getElementById("myModal1").style.display = "none";
}

/* When the user clicks anywhere outside of the modal, close it */
window.onclick = function (event) {
    var modal = document.getElementById("myModal1");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}



/////////button


function showInput(buttonId) {
    // Hide all input forms
    var inputDivs = document.getElementsByClassName("input-div");
    for (var i = 0; i < inputDivs.length; i++) {
        inputDivs[i].style.display = "none";
    }

    // Show the input form for the clicked button
    var inputDiv = document.getElementById("inputDiv" + buttonId.slice(-1));
    inputDiv.style.display = "block";
}

var submitButtons = document.getElementsByClassName("submit-btn");
for (var i = 0; i < submitButtons.length; i++) {
    submitButtons[i].addEventListener("click", function () {
        var buttonId = this.getAttribute("data-value");
        var inputField = document.getElementById("textInput" + buttonId.slice(-1));
        var messageDiv = this.nextElementSibling;

        // Get the value of the input field
        var inputValue = inputField.value;

        // Validate the input value
        if (inputValue === "") {
            messageDiv.innerHTML = "Please enter a bid amount.";
            return;
        }

        if (isNaN(inputValue)) {
            messageDiv.innerHTML = "Please enter a valid bid amount.";
            return;
        }

        // Submit the form
        messageDiv.innerHTML = "Your bid has been submitted.";

        // Hide the input field and the submit button
        inputField.style.display = "none";
        this.style.display = "none";
        // Here you can write your code to submit the bid to the server using Ajax or fetch API
    });
}





