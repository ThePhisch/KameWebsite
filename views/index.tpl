<%
import translate
t = translate.Translator()
t.setLang(p.currentLang)
%>

<html>
	<script>
		function toggleChangePassword() {
			var x = document.getElementById("formForPasswordChange");
			if (x.style.display === "none") {
				x.style.display = "block";
			}
			else {
				x.style.display = "none";
			}
		}
	</script>
	<head>
		<title>{{t.g('TEMPORARY_WEBSITE')}}</title>
		<link rel="stylesheet" href="/static/style.css">
	</head>
	<body>
		<div class="startDiv">
			<div class="splitsleft">
			<h1>{{t.g('TITLE')}}</h1>
			<a href="/?currentLang=de">Deutsch</a>
			<a href="/?currentLang=en">English</a>
			({{t.g('SETS_COOKIE')}})
			</div>
			<div class="rightStart">
			%if p.cookieTimeout:
			<h4>{{t.g('COOKIE_TIMEOUT')}}</h4>

			%elif p.uName == "":
				%if p.loginFail:
				<h4>{{t.g('LOGIN_FAILED')}}</h4>
				%else:
				<h4>{{t.g('LOGIN')}} ({{t.g('SETS_COOKIE')}}) ({{t.g('CURR_DEACTIVATED')}})</h4>
				%end
			<form action="/" method="post">
				{{t.g('USERNAME')}}: <input name="username" type="text" />
				{{t.g('PASSWORD')}}: <input name="password" type="password" />
				<input value="{{t.g('LOGIN')}}" type="submit" />
			</form>
			%else: # LOGGED ON
			<h4>{{t.g('LOGGED_IN_AS')}} {{p.uName}}</h4>
				%if p.passwordChanged:
				{{t.g('PASS_CHANGED')}}
				%elif p.passwordChangeError:
				{{t.g('PASS_CHANGE_ERROR')}}
				%elif p.passwordMismatch:
				{{t.g('PASS_CHANGE_MISMATCH')}}
				%end
			<form action="/" method="GET">
				<button name="logout" type="submit" value="1">{{t.g('LOG_OUT')}}</button>
			</form>
			<button onclick="toggleChangePassword()">{{t.g('PASS_CHANGE')}}</button>
			<form action="/" method="post" style="display: none;" id="formForPasswordChange">
				{{t.g('PASS_OLD')}}: <input name="oldPassword" type="password" />
				{{t.g('PASS_NEW')}}: <input name="newPassword" type="password" />
				{{t.g('PASS_NEW_REPEAT')}}: <input name="newPasswordConfirm" type="password" />
				<button name="changePassword" type="submit" value="1">{{t.g('PASS_CHANGE_SUBMIT')}}</button>
			</form>
			%end
			</div>
		</div>

		<hr>
		<div id="gameDiv">
			<iframe src="/game/KameWeb_s.htmlx" width="1000" height="600"></iframe>
		</div>
		<hr>
		<div id="updatesDiv">
			<h4>Updates</h4>
			<ol>
				<li>16.09.2020 0.3.1</li>
				<li>17.09.2020 0.3.1-webpatch1; kleine Änderungen, die auf erste Kommentare/Kritiken eingehen</li>
				<li>20.09.2020 Updated Server to 0.1</li>
				<li>20.09.2020 Updated Server to 0.1.1</li>
			</ol>
		</div>
		<div id="impressumDiv">
			<h4>Impressum/Kontakt</h4>
			Ohne Impressum, da private Webseite. Ich schalte keine Werbung, verkaufe nix und biete keine
			journalistischen Inhalte an. Standardmäßig werden keine Cookies gesetzt. Überall dort, wo Cookies
			gesetzt werden, wird darauf hingewiesen. Kontaktaufnahme erstmal über urinalgame (at) gmail (dot) com.
		</div>
	</body>
</html>
