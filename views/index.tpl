<%
import translate
t = translate.Translator()
t.setLang(p.currentLang)
loggedOn = False
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
			<div class="left">
				<div class="titlediv">
					<h1>{{t.g('TITLE')}}</h1>
				</div>
				<div class="belowtitle">
					<a href="/?currentLang=de">Deutsch</a>
					<a href="/?currentLang=en">English</a>
					({{t.g('SETS_COOKIE')}})
				</div>
			</div>
			<div class="right">
				<div class="titlediv">
					%if p.cookieTimeout:
						<span class="b">{{t.g('COOKIE_TIMEOUT')}}</span>
					%elif p.uName == "":
						%if p.loginFail:
						<span class="b">{{t.g('LOGIN_FAILED')}}</span>
						%else: # THIS IS THE STANDARD RESPONSE
						<span class="b">{{t.g('LOGIN')}} ({{t.g('SETS_COOKIE')}}) ({{t.g('ACTIVATED_NOTPUBLIC')}})</span>
						%end # SHOW LOGIN FORM
					%else: # LOGGED ON
						%loggedOn = True
						<span class="b">{{t.g('LOGGED_IN_AS')}} {{p.uName}}</span>
						%if p.passwordChanged:
							{{t.g('PASS_CHANGED')}}
						%elif p.passwordChangeError:
							{{t.g('PASS_CHANGE_ERROR')}}
						%elif p.passwordMismatch:
							{{t.g('PASS_CHANGE_MISMATCH')}}
						%end
					%end
				</div>
				<div class="belowtitle">
					%if loggedOn:
						<div class="uibuttons">
							<form action="/" method="GET">
								<button name="logout" type="submit" value="1">{{t.g('LOG_OUT')}}</button>
							</form>
							<button onclick="toggleChangePassword()">{{t.g('PASS_CHANGE')}}</button>
						</div>
					%else:
						<div>
							<form action="/" method="post">
								{{t.g('USERNAME')}}: <input name="username" type="text" />
								{{t.g('PASSWORD')}}: <input name="password" type="password" />
								<input value="{{t.g('LOGIN')}}" type="submit" />
							</form>
						</div>
					%end
				</div>
			</div>
			<form action="/" method="post" id="formForPasswordChange">
				{{t.g('PASS_OLD')}}: <input name="oldPassword" type="password" />
				{{t.g('PASS_NEW')}}: <input name="newPassword" type="password" />
				{{t.g('PASS_NEW_REPEAT')}}: <input name="newPasswordConfirm" type="password" />
				<button name="changePassword" type="submit" value="1">{{t.g('PASS_CHANGE_SUBMIT')}}</button>
			</form>
		</div>
		<hr>
		<div id="gameDiv">
			<iframe src="/game/KameWeb_s.htmlx" width="1000" height="600"></iframe>
			<!-- <iframe src="/game/KameWeb0-3-2.tpl" width="1000" height="600"></iframe> -->
		</div>
		<hr>
		<div id="updatesDiv">
			<h4>Updates</h4>
			<ol>
				<li>16.09.2020 0.3.1</li>
				<li>17.09.2020 0.3.1-webpatch1; kleine Änderungen, die auf erste Kommentare/Kritiken eingehen</li>
				<li>20.09.2020 Updated Server to 0.1</li>
				<li>20.09.2020 Updated Server to 0.1.1</li>
				<li>24.09.2020 Updated Server to 0.1.2</li>
				<li>24.09.2020 0.3.2</li>
				<li>25.09.2020 Fixed Server Issue with SQL (thanks, Kumiko)</li>
				<li>26.09.2020 Fixed Server Issue with SQL</li>
			</ol>
		</div>
		<div id="impressumDiv">
			<h4>Impressum/Kontakt</h4>
			Ohne Impressum, da private Webseite. Ich schalte keine Werbung, verkaufe nix und biete keine
			journalistischen Inhalte an. Standardmäßig werden keine Cookies gesetzt. Überall dort, wo Cookies
			gesetzt werden, wird darauf hingewiesen. Bei eingeloggten Nutzern wird der Spielfortschritt
			gespeichert, ansonsten werden keine personenbezogenen Daten erhoben.
			Kontaktaufnahme erstmal über urinalgame (at) gmail (dot) com, dort können auch neue Nutzerkonten
			angefordert werden.
		</div>
	</body>
</html>
