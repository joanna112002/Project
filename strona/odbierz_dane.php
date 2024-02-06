<?php
// Pobranie danych z formularza
$imie = $_POST['imie'];
$email = $_POST['email'];
$wiadomosc = $_POST['wiadomosc'];

// Połączenie z bazą danych
$server="localhost";
$user="joanna.palka";
$password="myyM34Ysql";
$db="joanna.palka";

$conn = new mysqli($server, $user, $password, $db);
if ($conn->connect_error) {
    die("Błąd połączenia z bazą danych: " . $conn->connect_error);
}

// Wstawienie danych do tabeli
$sql = "INSERT INTO wiadomosci (imie, email, wiadomosc) VALUES ('$imie', '$email', '$wiadomosc')";

if ($conn->query($sql) === TRUE) {
    echo "<script>location.href='https://ux.up.krakow.pl/~joanna.palka/strona/opinie.php'</script>";
    // header("Location https://ux.up.krakow.pl/~joanna.palka/strona/rezerwacja.html");
    exit();
    // echo "Wiadomość została wysłana i zapisana.";
} else {
    echo "Błąd podczas zapisywania wiadomości: " . $conn->error;
}

$conn->close();
?>
