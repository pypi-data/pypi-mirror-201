# Rapid Innovation Package

Rapid Innovation is a Python package that provides a set of tools and utilities for rapid development and innovation.

## Installation

To install Rapid Innovation, simply run:

        pip install rapid_innovation

## Usage

To use Rapid Innovation, simply import the desired module and call the desired function or class. For example:

        !pip install rapid-innovation
        from rapid.email import RapidEmailNotificationSMTP
        
        smtp_user = 'XXXXXXX'
        smtp_password = 'XXXXXX'
        
        renstmp = RapidEmailNotificationSMTP(smtp_user, smtp_password)
        
        to = ['abhisheknegi@rapidinnovation.dev']
        subject = 'Pip Package testing'
        content = 'Testing upload pip package.'
        
        renstmp.send_email(to, subject, content)



## License

Rapid Innovation is released under the MIT License.