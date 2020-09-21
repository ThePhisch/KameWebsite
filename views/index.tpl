<%
import translate
t = translate.Translator()
t.setLang(p.currentLang)
%>

<html>
	<head>
		<title>Vorläufige Webseite</title>
		<link rel="stylesheet" href="/static/style.css">
	</head>
	<body>
		<div id="startDiv">
			<div class="splits">
			<h1>{{t.g('TITLE')}}</h1>
			<a href="/?currentLang=de">Deutsch</a>
			<a href="/?currentLang=en">English</a>
			({{t.g('SETS_COOKIE')}})
			</div>
			<div class="splits rightStart">
			%if p.cookieTimeout:
			<h4>Cookie Timeout</h4>

			%elif p.uName == "":
				%if p.loginFail:
				<h4>Login Failed</h4>
				%else:
				<h4>{{t.g('LOGIN')}} ({{t.g('SETS_COOKIE')}}) ({{t.g('CURR_DEACTIVATED')}})</h4>
				%end
			<form action="/" method="post">
				{{t.g('USERNAME')}}: <input name="username" type="text" />
				{{t.g('PASSWORD')}}: <input name="password" type="password" />
				<input value="{{t.g('LOGIN')}}" type="submit" />
			</form>
			%else: # LOGGED ON
			<h4>{{p.uName}}</h4>
			<form action="/" method="GET">
				<button name="logout" type="submit" value="1">Logout</button>
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
