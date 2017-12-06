<?php

//create short variables
$old_passwd = $HTTPS_POST_VARS['old_passwd'];
$new_passwd = $HTTPS_POST_VARS['new_passwd'];
$new_passwd2 = $HTTPS_POST_VARS['new_passwd2'];

function check_valid_user()
{
    
}
if(!filled_out($HTTPS_POST_VARS))
{
    echo 'You have not filled out the form completely.
            Please try again';
    display_user_menu();
    do_html_footer();
    exit;
}
else{
    if($new_passwd != $newpasswd2)
        echo "Passwords entered were not the same.Not changed";
    else if(strlen($new_passwd) > 16 || strlen($new_passwd) <6)
        echo 'New password must be between 6 and 16 characters. Try again';
    else{
        //attempt update
        if(change_password($HTTPS_SESSION_VARS['valid_user'], $old_passwd,
                            $new_passwd))
            echo 'Password changed.';
        else{
            echo "Password could not be changed";
        }
    }
}

display_user_menu();
do_html_footer();

?>