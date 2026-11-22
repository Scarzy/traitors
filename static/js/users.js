var insert_roles_buttons = function (cell, index, role) {
	let faithfulbutton = document.createElement("INPUT")
	faithfulbutton.type = "radio"
	faithfulbutton.classList.add("btn-check")
	faithfulbutton.name = "options-".concat(index)
	faithfulbutton.id = "faithfuloption-".concat(index)
	faithfulbutton.setAttribute("autocomplete", "off")
	faithfulbutton.checked = true
	let faithfullabel  = document.createElement("LABEL")
	faithfullabel.classList.add("btn")
	faithfullabel.classList.add("btn-secondary")
	faithfullabel.innerHTML = "Faithful"
	faithfullabel.setAttribute("for", "faithfuloption-".concat(index))
	let traitorbutton = document.createElement("INPUT")
	traitorbutton.type = "radio"
	traitorbutton.classList.add("btn-check")
	traitorbutton.name = "options-".concat(index)
	traitorbutton.id = "traitoroption-".concat(index)
	traitorbutton.setAttribute("autocomplete", "off")
	let traitorlabel  = document.createElement("LABEL")
	traitorlabel.classList.add("btn")
	traitorlabel.classList.add("btn-secondary")
	traitorlabel.innerHTML = "Traitor"
	traitorlabel.setAttribute("for", "traitoroption-".concat(index))
	cell.appendChild(faithfulbutton)
	cell.appendChild(faithfullabel)
	cell.appendChild(traitorbutton)
	cell.appendChild(traitorlabel)

}

var get_users = function() {
	fetch("/users")
	.then(res => res.json())
	.then(out => out.forEach(
			function(user, i) {
				var row = document.getElementById("userstable").insertRow(-1)
				row.insertCell(0).innerHTML = user["name"]
				insert_roles_buttons(row.insertCell(1), i, user["role"])
				row.classList.add("text-light")
			}
		)
	)
	.catch(err => console.log(err))
}
