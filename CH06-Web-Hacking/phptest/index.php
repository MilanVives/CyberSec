<?php
// debug_index.php - lab only
error_reporting(E_ALL);
ini_set('display_errors',1);
$filename = isset($_GET['filename']) ? $_GET['filename'] : '';
echo "<p>Requested filename: " . htmlspecialchars($filename) . "</p>";

$built = __DIR__ . '/files/' . $filename;
echo "<p>Built path: " . htmlspecialchars($built) . "</p>";

$rp = realpath($built);
echo "<p>realpath(): " . ($rp ? htmlspecialchars($rp) : 'FALSE') . "</p>";
echo "<p>file_exists: " . (file_exists($built) ? 'true' : 'false') . "</p>";
echo "<p>is_readable: " . (is_readable($built) ? 'true' : 'false') . "</p>";

if (file_exists($built) && is_readable($built)) {
    echo "<h2>Contents:</h2><pre>" . htmlspecialchars(file_get_contents($built)) . "</pre>";
} else {
    echo "<p>File not found or not readable!</p>";
}
?>
