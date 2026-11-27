const score_user = function (user, index) {
	const scoreId = `scoreoption-${index}`;
	let score = document.getElementById(scoreId).value;
	fetch(`/scores/`.concat(user["id"]), {
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

const insert_action_buttons = function (cell, index, user) {
	const scoreId = `scoreoption-${index}`;
	
	const div = document.createElement("DIV");
	div.classList.add("input-group", "mb-3");

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

	div.appendChild(scorelabel);
	div.appendChild(scoreselect);
	div.appendChild(scorebutton);
	
	cell.appendChild(div);
};

const get_scores = function () {
	fetch("/scores")
		.then(res => res.json())
		.then(out => {
				const tbody = document.getElementById("userstable");
				const fragment = document.createDocumentFragment();
				out.forEach(
					function (user, i) {
						var row = document.createElement("tr");
						row.insertCell(0).innerHTML = user["name"];
						insert_action_buttons(row.insertCell(1), i, user);
						row.classList.add("text-light");
						fragment.appendChild(row);
					}
			)
			tbody.replaceChildren(fragment);
		})
		.catch(err => console.log(err));
};

