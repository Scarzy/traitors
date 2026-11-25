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

const score_user = function (user, index) {
	const scoreId = `scoreoption-${index}`;
	let score = document.getElementById(scoreId).value;
	fetch(`/action/`.concat(user["id"]), {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ action: "score", score: score })
	})
	.then(res => {
		if (!res.ok) {
			throw new Error(`Server error: ${res.status}`);
		} else {
			document.getElementById(scoreId).value = 0;
		}
		return res.json();
	})
	.then(data => console.log(`Updated ${user.name} score by ${score}`, data))
	.catch(err => console.error("Failed to update score:", err));
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

const perform_major_action = function (action) {
	fetch(`/majoraction`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ action: action })
	})
	.then(res => {
		if (!res.ok) throw new Error(`Server error: ${res.status}`);
		return res.json();
	})
	.then(data => console.log(`Performed action ${action}`, data))
	.then(get_users())
	.catch(err => console.error("Failed to perform action:", err));
};

const add_major_action_listeners = function () {
	document.getElementById("dayturnover").addEventListener("click", () => perform_major_action("dayturnover"));
};

const insert_roles_buttons = function (cell, index, user) {
	const faithfulId = `faithfuloption-${index}`;
	const traitorId = `traitoroption-${index}`;
	
	const div = document.createElement("DIV");
	div.classList.add("input-group", "mb-3");
	
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

	div.appendChild(faithfulbutton);
	div.appendChild(faithfullabel);
	div.appendChild(traitorbutton);
	div.appendChild(traitorlabel);
	
	cell.appendChild(div);
};

const insert_action_buttons = function (cell, index, user) {
	const murderId = `murderoption-${index}`;
	const banishId = `banishoption-${index}`;
	const recruitId = `recruitoption-${index}`;
	const scoreId = `scoreoption-${index}`;
	
	const div = document.createElement("DIV");
	div.classList.add("input-group", "mb-3");

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

	const scorelabel = document.createElement("LABEL");
	scorelabel.classList.add("input-group-text");
	scorelabel.innerHTML = "Score";
	scorelabel.setAttribute("for", scoreId);
	
	const scoreselect = document.createElement("SELECT");
	scoreselect.classList.add("form-select");
	scoreselect.id = scoreId;
	for (let i = 100; i >= -100; i = i - 10) {
		var option = document.createElement("OPTION");
		option.text = i;
		option.value = i;
		if (i == 0) {
			option.selected = true;
		}
		scoreselect.add(option);
	}

	const scorebutton = document.createElement("BUTTON");
	scorebutton.type = "button";
	scorebutton.classList.add("btn");
	scorebutton.classList.add("btn-dark");
	scorebutton.innerHTML = "Submit score";
	scorebutton.addEventListener("click", () => score_user(user, index));

	div.appendChild(murderbutton);
	div.appendChild(recruitbutton);
	div.appendChild(banishbutton);
	
	div.appendChild(scorelabel);
	div.appendChild(scoreselect);
	div.appendChild(scorebutton);
	
	cell.appendChild(div);
};

const get_users = function () {
	fetch("/users")
		.then(res => res.json())
		.then(out => {
				const tbody = document.getElementById("userstable");
				const fragment = document.createDocumentFragment();
				out.forEach(
					function (user, i) {
						var row = document.createElement("tr");
						row.insertCell(0).innerHTML = user["name"];
						insert_roles_buttons(row.insertCell(1), i, user);
						insert_action_buttons(row.insertCell(2), i, user);
						row.classList.add("text-light");
						fragment.appendChild(row);
					}
			)
			tbody.replaceChildren(fragment);
		})
		.catch(err => console.log(err));
};

