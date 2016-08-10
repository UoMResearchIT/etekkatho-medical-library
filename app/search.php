<?php
    $query  = $_GET['q'];
    $start  = (is_numeric($_GET['start'])) ? $_GET['start']: 0;
    $rows   = 50;
    $results = json_decode(file_get_contents('http://localhost:8983/solr/pubmed/query?start='.$start.'&rows='.$rows.'&q='.urlencode($query)));
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Meta -->
    <meta charset="utf-8">
    <title>eTekkatho Medical Library</title>
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Mobile Specific Meta -->
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- CSS -->
    <link rel="stylesheet" href="css/normalize.css">
    <link rel="stylesheet" href="css/skeleton.css">
    <link rel="stylesheet" href="css/style.css">

    <!-- Favicon -->
    <!-- IE -->
    <link rel="shortcut icon" type="image/x-icon" href="img/favicon.ico" />
    <!-- other browsers -->
    <link rel="icon" type="image/x-icon" href="img/favicon.ico" />
</head>
<body>
    <div id="header-wrapper">
        <div class="container">
            <div class="row" id="header">
                <a href="/">
                    <img src=" data:image/png;base64,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" alt="eTekkatho logo - Myanmar language version" width="139" height="61" />
                </a>
                <span id="page-title">eTekkatho Medical Library</span>
            </div>
        </div>
        
        <div class="container">
            <div class="row">
                <form action="search.php" method="get">
                    <div class="nine columns">
                        <input name="q" id="search-text" type="search" maxlength="100" placeholder="Find PubMed articles..." value="<?php echo $query; ?>">
                    </div>
                    <div class="three columns">
                        <button type="submit" id="search-button">Find articles</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <div class="container" id="search-results">
        <div class="row">
        <?php
        if($query == '') {
            $title = '<h5><span style="color:red">Please enter a search term</span></h5>';
        } else {
            $title = '<h5>Found '.$results->response->numFound.' results for '.$query.':</h5>';
        }
        echo $title;
        ?>
        </div>
        
        <?php if($query != '' && $results->response->numFound > 0): ?>
        <div class="row" id="results-range">
            <?php
                if(is_numeric($_GET['start'])) {
                    $start = $_GET['start'];
                    $end = $start+50;
                    $end = ($end > $results->response->numFound) ? $results->response->numFound: $end;
                    
                    $offset = $start+50;
                    
                    if(($offset) > $results->response->numFound) {
                        $nextPage = '';
                    } else {
                        $nextPage = '<a href="/search.php?q='.$query.'&start='.$offset.'&rows=50">Next page &raquo;</a>';
                    }
                    
                    $start = ($start == 0) ? 1: $start;
                    echo 'Displaying '.$start.' to '.$end.' articles. '.$nextPage;
                } else {
                    $next = 50;
                    $end = ($results->response->numFound < 50) ? $results->response->numFound: 50;
                    echo 'Displaying 1 to '.$end.' articles. <a href="/search.php?q='.$query.'&start='.$next.'&rows=50">Next page &raquo;</a>';
                }
            ?>
        </div>
        <?php endif; ?>
    </div>
    
    <div class="container" id="results-list">
        <div class="row">
            <div class="nine columns">
            <?php
            // Parse the Solr $results
            foreach($results->response->docs as $row) {
                echo '<div class="result">';
                echo '<h6><a href="/pubmed/'.$row->{'filename'}[0].'">'.$row->{'article-title'}[0].'</a> <span class="result-year">(YYYY)</span></h6>';
                
                echo '<p>Abstract snippet, lorem ipsum dolor sit amet, accusam commune aliquando cum at. Illum consequat quo ei, nominati appellantur vel ut. Mutat legendos constituam pro ei, ea amet omnium pri. Sea in causae legimus, sale labitur tractatos eum ad, eu ius porro complectitur. Sed id delicata molestiae. Maiorum mediocrem ut est.</p>';
                
                echo '
                <table class="u-full-width">
                    <tbody>
                    <tr>
                        <td>Publication:</td>
                        <td>'.$row->{'journal-title'}[0].'</td>
                    </tr>
                    <tr>
                        <td>Link: </td>
                        <td><a href="http://'.$_SERVER[HTTP_HOST].'/pubmed/'.$row->{'filename'}[0].'">http://'.$_SERVER[HTTP_HOST].'/pubmed/'.$row->{'filename'}[0].'</a> (PDF)</td>
                    </tr>
                    <tr>
                        <td>Authors:</td><td>';
                        
                        if(strlen($row->{'authors'}[0]) > 0) {
                            echo implode(', ', explode(',', $row->{'authors'}[0]));
                        }
                        
                echo'</td>
                    </tr>
                    </tbody>
                </table>
                ';
                
                echo '</div>';
            }
            ?>
            </div>
            
            <?php if($query != '' && $results->response->numFound > 0): ?>
            <div class="three columns">
                <div id="results-filter">
                    <h4>Filter results</h4>
                    <p>Select year range</p>
                    ...
                </div>
            </div>
            <?php endif; ?>
        </div>
    </div>
    
    <?php if($query != '' && $results->response->numFound > 0): ?>
    <div class="container" id="results-pages">
        <div class="row">
            <div class="nine columns">
                <nav><span>Results pages:<br></span>
                <?php
                    $pages = ceil($results->response->numFound/50);
                
                    for($i=0; $i<$pages;$i++) {
                        if($i > 2 && $i%20 == 0) {
                            $linebreak = '<br>';
                        } else {
                            $linebreak = '';
                        }
                    
                        $offset = $i*50;
                        $page = $i+1;
                        echo '<a href="/search.php?q='.$query.'&start='.$offset.'&rows=50">'.$page.'</a>'.$linebreak;
                    }
                ?>
                </nav>
            </div>
        </div>
    </div>
    <?php endif; ?>
</body>
</html>
