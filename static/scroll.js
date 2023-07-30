

const observer = new IntersectionObserver((entries) => {
    console.log("Iterating")
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            console.log("Intersecting")
            entry.target.classList.add('show')
        }
    })
})

var hiddenElements = document.querySelectorAll('.hidden')
hiddenElements.forEach((el) => observer.observe(el))


console.log("Conneceted")
/*
const observer = new IntersectionObserver((entries) => {
    console.log("Iterating")
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            console.log("Intersecting")
            entry.target.classList.remove('hidden')
        }
    })
})
*/