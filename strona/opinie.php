<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
         body {
            font-family: Arial, sans-serif;
            background-color: #f1e1e1;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #c4b9b9;
            padding: 20px;
            text-align: center;
        }

        h1 {
            font-size: 30px;
            color: #333;
            margin-bottom: 10px;
        }

        nav ul {
            list-style-type: none;
        }

        nav li {
            display: inline;
            margin-right: 20px;
        }

        nav a {
            text-decoration: none;
            color: #666;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }

        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .menu-icon {
    display: none;
}

@media only screen and (max-width: 600px) {
    .usluga {
        width: 100%;
    }
}

.menu-icon {
    display: none;
}

@media screen and (max-width: 768px) {
    .menu-icon {
        display: block;
    }

    nav ul {
        display: none;
        text-align: center;
    }

    nav li {
        display: block;
        margin: 10px 0;
    }
}

/* Style dla responsywnego menu */
.menu-icon {
    font-size: 24px;
    cursor: pointer;
}

nav ul.show {
    display: block;
}
        
    </style>
</head>
<body>
    <header>
        <h1>Zakład Groomerski</h1>
        <h2>Najlepszy zakład na Podhalu</h2>
        <nav>
        <div class="menu-icon">&#9776;</div>
            <ul>
                <li><a href="strona.html">Strona główna</a></li>
                <li><a href="usługi.html">Usługi</a></li>
                <li><a href="galeria.html">Galeria</a></li>
                <li><a href="kontakt.html">Kontakt</a></li>
                <li><a href="opinie.php">Opinie</a></li>
            </ul>
        </nav>
    </header>

    <script>

        // Skrypt obsługujący rozwijanie i zwijanie menu dla małych ekranów
        var menuIcon = document.querySelector('.menu-icon');
        var menuList = document.querySelector('nav ul');

        menuIcon.addEventListener('click', function() {
            menuList.classList.toggle('show');
        });
    </script>

    <?php
    $server = "localhost";
    $user = "joanna.palka";
    $password = "myyM34Ysql";
    $db = "joanna.palka";

    $conn = new mysqli($server, $user, $password, $db);

    if ($conn->connect_error) {
        die("Błąd połączenia z bazą danych: " . $conn->connect_error);
    }

    if (isset($_POST["imie"])) {
        $imie = $_POST['imie'];
        $email = $_POST['email'];
        $wiadomosc = $_POST['wiadomosc'];
        $data_czas = date('Y-m-d H:i:s'); // Aktualna data i czas
        $sql2 = "INSERT INTO wiadomosci (imie, email, wiadomosc, data_czas) VALUES ('$imie', '$email', '$wiadomosc', '$data_czas');";
        $wynik2 = $conn->query($sql2);
        if (!$wynik2) {
            echo "Błąd w zapytaniu: " . $conn->error;
        }
        echo "Zapytanie wykonane poprawnie.";
    }

    if (isset($_POST["id_do_usuniecia"])) {
        $id_do_usuniecia = $_POST['id_do_usuniecia'];
        $sql3 = "DELETE FROM wiadomosci WHERE id = $id_do_usuniecia;";
        $wynik3 = $conn->query($sql3);
        if (!$wynik3) {
            echo "Błąd w zapytaniu: " . $conn->error;
        }
        
    }

    $sql = "SELECT * FROM wiadomosci";
    $wynik = $conn->query($sql);
    if (!$wynik) {
        echo "Błąd w zapytaniu: " . $conn->error;
    }
    ?>

    <table>
        <tr>
            <th>Imię</th>
            <th>Email</th>
            <th>Wiadomość</th>
            <th>Data dodania</th>
            <th>Akcje</th>
        </tr>
        <?php
        while ($wiersz = $wynik->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $wiersz['imie'] . "</td>";
            echo "<td>" . $wiersz['email'] . "</td>";
            echo "<td>" . $wiersz['wiadomosc'] . "</td>";
            echo "<td>" . $wiersz['data_czas'] . "</td>";
            echo '<td>
                <form method="POST">
                    <input type="hidden" name="id_do_usuniecia" value="' . $wiersz['id'] . '">
                    <input type="submit" value="Usuń">
                </form>
            </td>';
            echo "</tr>";
        }
        ?>
    </table>

    <?php
    $conn->close();
    ?>
</body>
</html>
