var get_whoami = function() {
	fetch("/whoami")
	.then(res => res.json())
	.then(out => {
			document.getElementById("users_name").innerHTML = out[0]["name"]
			document.getElementById("users_score").innerHTML = out[0]["score"]
			document.getElementById("users_role").innerHTML = out[0]["role"]
		}
	)
	.catch(err => console.log(err))
}

var start_timers = function() {
	setInterval(get_whoami, 60000);
	setInterval(get_voting_valid, 1000);
}

var get_voting_valid = function() {
	fetch("/votingtime")
	.then(res => res.json())
	.then(out => {
			document.getElementById("murderoption").setAttribute("aria-disabled",(out["murderthreshold"] > 0) ? "true" : "false")
			document.getElementById("banishoption").setAttribute("aria-disabled",(out["banishthreshold"] > 0) ? "true" : "false")
		}
	)
	.catch(err => console.log(err))
}
