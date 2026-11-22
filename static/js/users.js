const update_role = function (user, newRole) {
	fetch(`/users/`.concat(user["id"]), {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ role: newRole })
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error: ${res.status}`);
		return res.json();
	})
	.then(data => console.log(`Updated ${user.name} to ${newRole}`, data))
	.catch(err => console.error("Failed to update role:", err));
};

const perform_action = function (user, action) {
	fetch(`/action/`.concat(user["id"]), {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ action: action })
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error: ${res.status}`);
		return res.json();
	})
	.then(data => console.log(`Updated ${user.name} to ${action}`, data))
	.catch(err => console.error("Failed to update role:", err));
};

const insert_roles_buttons = function (cell, index, user) {
	const faithfulId = `faithfuloption-${index}`;
	const traitorId = `traitoroption-${index}`;

	const faithfulbutton = document.createElement("INPUT");
	faithfulbutton.type = "radio";
	faithfulbutton.classList.add("btn-check");
	faithfulbutton.name = `options-${index}`;
	faithfulbutton.id = faithfulId;
	faithfulbutton.setAttribute("autocomplete", "off");
	faithfulbutton.checked = (user.role === "faithful");
	faithfulbutton.addEventListener("change", () => update_role(user, "faithful"));

	const faithfullabel = document.createElement("LABEL");
	faithfullabel.classList.add("btn", "btn-secondary");
	faithfullabel.innerHTML = "Faithful";
	faithfullabel.setAttribute("for", faithfulId);

	const traitorbutton = document.createElement("INPUT");
	traitorbutton.type = "radio";
	traitorbutton.classList.add("btn-check");
	traitorbutton.name = `options-${index}`;
	traitorbutton.id = traitorId;
	traitorbutton.setAttribute("autocomplete", "off");
	traitorbutton.checked = (user.role === "traitor");
	traitorbutton.addEventListener("change", () => update_role(user, "traitor"));

	const traitorlabel = document.createElement("LABEL");
	traitorlabel.classList.add("btn", "btn-secondary");
	traitorlabel.innerHTML = "Traitor";
	traitorlabel.setAttribute("for", traitorId);

	cell.appendChild(faithfulbutton);
	cell.appendChild(faithfullabel);
	cell.appendChild(traitorbutton);
	cell.appendChild(traitorlabel);
};

const insert_action_buttons = function (cell, index, user) {
	const murderId = `murderoption-${index}`;
	const banishId = `banishoption-${index}`;
	const recruitId = `recruitoption-${index}`;

	const murderbutton = document.createElement("BUTTON");
	murderbutton.type = "button";
	murderbutton.classList.add("btn");
	murderbutton.classList.add("btn-danger");
	murderbutton.id = murderId;
	murderbutton.innerHTML = "Murder";
	murderbutton.addEventListener("click", () => perform_action(user, "murder"));

	const recruitbutton = document.createElement("BUTTON");
	recruitbutton.type = "button";
	recruitbutton.classList.add("btn");
	recruitbutton.classList.add("btn-warning");
	recruitbutton.id = recruitId;
	recruitbutton.innerHTML = "Recruit";
	recruitbutton.addEventListener("click", () => perform_action(user, "recruit"));

	const banishbutton = document.createElement("BUTTON");
	banishbutton.type = "button";
	banishbutton.classList.add("btn");
	banishbutton.classList.add("btn-dark");
	banishbutton.id = banishId;
	banishbutton.innerHTML = "Banish";
	banishbutton.addEventListener("click", () => perform_action(user, "banish"));

	cell.appendChild(murderbutton);
	cell.appendChild(recruitbutton);
	cell.appendChild(banishbutton);
};

const get_users = function () {
	fetch("/users")
		.then(res => res.json())
		.then(out => out.forEach(
			function (user, i) {
				const row = document.getElementById("userstable").insertRow(-1);
				row.insertCell(0).innerHTML = user["name"];
				insert_roles_buttons(row.insertCell(1), i, user);
				insert_action_buttons(row.insertCell(2), i, user);
				row.classList.add("text-light");
			}
		))
		.catch(err => console.log(err));
};

