from flask import Flask, render_template, request

app = Flask(__name__)

DEVICES = {
    'laptop': {
        'name': 'Laptop',
        'icon': '💻',
        'environmental_impact': 'A single laptop contains up to 60 different elements, including rare earth metals. Improper disposal leaches lead, mercury, and cadmium into soil and groundwater. Recycling one laptop recovers enough aluminium to produce 4 beverage cans.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Back up your data',
                'detail': 'Copy everything you want to keep to an external drive or cloud storage before proceeding.'
            },
            {
                'step': 2,
                'title': 'Sign out of all accounts',
                'detail': 'Sign out of your email, browser, cloud services (iCloud, Google, OneDrive), and any apps that store credentials.'
            },
            {
                'step': 3,
                'title': 'Deauthorise software licences',
                'detail': 'Deactivate Adobe, Microsoft Office, or any other licensed software before wiping — you may need to reuse those licences.'
            },
            {
                'step': 4,
                'title': 'Perform a factory reset or secure wipe',
                'detail': 'Windows: Settings → System → Recovery → Reset this PC → Remove everything. macOS: Boot into Recovery Mode → Disk Utility → Erase, then reinstall macOS. For sensitive data, use DBAN or similar tool for a multi-pass overwrite.'
            },
            {
                'step': 5,
                'title': 'Verify the wipe was successful',
                'detail': 'Boot the device after reset and confirm no personal files or accounts remain. Check Documents, Downloads, Desktop, and browser history.'
            },
            {
                'step': 6,
                'title': 'Remove any external media',
                'detail': 'Check for and remove any SD cards, USB drives, or SIM cards still inserted in the device.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'TechCollect',
                'description': 'Free drop-off for computers and accessories at 600+ locations across Australia.',
                'url': 'https://techcollect.com.au',
                'covers': 'Laptops, desktops, monitors, keyboards, mice'
            },
            {
                'name': 'Council E-waste Programs',
                'description': 'Most Australian councils run free e-waste collection events. Check your local council website for dates.',
                'url': 'https://www.sustainability.vic.gov.au',
                'covers': 'Most electronic devices'
            },
            {
                'name': 'Manufacturer Take-Back',
                'description': 'Apple, Dell, HP, and Lenovo all offer trade-in or recycling programs. Check your manufacturer\'s website directly.',
                'url': 'https://www.apple.com/au/shop/trade-in',
                'covers': 'Brand-specific devices'
            }
        ]
    },
    'smartphone': {
        'name': 'Smartphone',
        'icon': '📱',
        'environmental_impact': 'Smartphones contain gold, silver, platinum, and palladium — mining these materials generates enormous environmental damage. If every Australian recycled their old phone, we\'d recover enough gold to fill a small swimming pool. Currently, less than 10% of phones are recycled.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Back up your data',
                'detail': 'Use iCloud, Google Backup, or connect to a computer to back up photos, contacts, messages, and app data.'
            },
            {
                'step': 2,
                'title': 'Remove your SIM and memory cards',
                'detail': 'Physically remove your SIM card and any microSD card before handing over the device.'
            },
            {
                'step': 3,
                'title': 'Sign out of all accounts',
                'detail': 'iPhone: Settings → Sign out of Apple ID. Android: Settings → Accounts → Remove all accounts. This is critical to prevent Activation Lock issues.'
            },
            {
                'step': 4,
                'title': 'Unpair Bluetooth devices',
                'detail': 'Remove paired devices including smartwatches, earbuds, and car systems.'
            },
            {
                'step': 5,
                'title': 'Factory reset the device',
                'detail': 'iPhone: Settings → General → Transfer or Reset iPhone → Erase All Content. Android: Settings → General Management → Reset → Factory Data Reset.'
            },
            {
                'step': 6,
                'title': 'Verify reset completed',
                'detail': 'Confirm the phone shows the initial setup screen and no personal data remains.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'MobileMuster',
                'description': 'Australia\'s official mobile phone recycling program. Free drop-off at 3,500+ locations including Australia Post and Officeworks.',
                'url': 'https://www.mobilemuster.com.au',
                'covers': 'Phones, batteries, chargers, accessories'
            },
            {
                'name': 'Telstra, Optus, Vodafone Store Drop-Off',
                'description': 'All major telcos accept old phones in-store for recycling at no charge.',
                'url': 'https://www.mobilemuster.com.au/drop-off-locations',
                'covers': 'All mobile phones regardless of brand or carrier'
            },
            {
                'name': 'Officeworks Tech Trade & Recycle',
                'description': 'Drop off old phones at any Officeworks store for free recycling.',
                'url': 'https://www.officeworks.com.au/information/sustainability',
                'covers': 'Phones, tablets, small electronics'
            }
        ]
    },
    'hard_drive': {
        'name': 'Hard Drive / SSD',
        'icon': '💾',
        'environmental_impact': 'Hard drives contain aluminium platters, rare earth magnets, and circuit boards loaded with hazardous materials. The rare earth elements in drive magnets are mined in processes that generate toxic radioactive waste. A recycled hard drive recovers aluminium, steel, and precious metals that would otherwise require destructive mining.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Identify what\'s on the drive',
                'detail': 'Before wiping, confirm whether the drive contains sensitive personal data, work files, financial records, or credentials.'
            },
            {
                'step': 2,
                'title': 'Back up anything you need',
                'detail': 'Copy any files you want to keep to another storage device before proceeding with sanitisation.'
            },
            {
                'step': 3,
                'title': 'For HDDs: perform a multi-pass overwrite',
                'detail': 'Use DBAN (Darik\'s Boot and Nuke) for a DoD 5220.22-M standard wipe. A single pass is sufficient for most personal use; 3-7 passes for sensitive data. This physically overwrites every sector.'
            },
            {
                'step': 4,
                'title': 'For SSDs: use manufacturer secure erase',
                'detail': 'Standard overwrite tools are not reliable on SSDs due to wear-levelling. Use the manufacturer\'s SSD toolbox (Samsung Magician, WD Dashboard, etc.) for a Secure Erase command, which is the only reliable method for SSDs.'
            },
            {
                'step': 5,
                'title': 'For maximum assurance: physical destruction',
                'detail': 'For highly sensitive data, physical destruction (degaussing or shredding) is the only guaranteed method. Many e-waste recyclers offer certified hard drive destruction with documentation.'
            },
            {
                'step': 6,
                'title': 'Document the sanitisation',
                'detail': 'Record the make, model, serial number, method used, and date of sanitisation. This is especially important for work or business drives.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'TechCollect',
                'description': 'Free drop-off for hard drives and storage devices at 600+ locations Australia-wide.',
                'url': 'https://techcollect.com.au',
                'covers': 'HDDs, SSDs, USB drives, optical drives'
            },
            {
                'name': 'Certified Data Destruction Services',
                'description': 'For business or sensitive drives, use a certified destruction service that provides a certificate of destruction.',
                'url': 'https://www.naid.org/find-a-member',
                'covers': 'All storage media with certified chain of custody'
            },
            {
                'name': 'Computer Recyclers Australia',
                'description': 'Specialist e-waste recyclers that handle data-bearing devices with documented destruction.',
                'url': 'https://www.computerrecyclers.com.au',
                'covers': 'All computer components and storage media'
            }
        ]
    },
    'tablet': {
        'name': 'Tablet',
        'icon': '📲',
        'environmental_impact': 'Tablets combine the environmental issues of both laptops and smartphones. Their lithium batteries are a particular concern — improperly disposed lithium batteries can cause fires in landfill and waste collection vehicles. Australia generates over 3,300 tonnes of battery waste annually.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Back up your data',
                'detail': 'Sync photos, documents, and app data to cloud storage or a computer before resetting.'
            },
            {
                'step': 2,
                'title': 'Remove SIM and memory cards',
                'detail': 'If your tablet has a SIM card slot or microSD slot, remove these before disposal.'
            },
            {
                'step': 3,
                'title': 'Sign out of all accounts',
                'detail': 'iPad: Settings → Your Name → Sign Out. Android: Settings → Accounts → Remove all. Removing your Apple ID or Google account is essential to disable Find My / Device Protection.'
            },
            {
                'step': 4,
                'title': 'Unpair connected devices',
                'detail': 'Remove paired Bluetooth accessories including keyboards, styluses, and smartwatches.'
            },
            {
                'step': 5,
                'title': 'Factory reset',
                'detail': 'iPad: Settings → General → Transfer or Reset iPad → Erase All. Android: Settings → General Management → Reset → Factory Data Reset.'
            },
            {
                'step': 6,
                'title': 'Confirm reset and check for accessories',
                'detail': 'Verify the device shows the setup screen. Remove any cases or screen protectors if recycling separately.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'TechCollect',
                'description': 'Accepts tablets at 600+ drop-off locations across Australia for free.',
                'url': 'https://techcollect.com.au',
                'covers': 'Tablets and accessories'
            },
            {
                'name': 'MobileMuster',
                'description': 'Accepts tablets as part of their mobile device recycling program.',
                'url': 'https://www.mobilemuster.com.au',
                'covers': 'Tablets, phones, and accessories'
            },
            {
                'name': 'Apple Trade In',
                'description': 'Apple offers trade-in credit or free recycling for iPad devices regardless of condition.',
                'url': 'https://www.apple.com/au/shop/trade-in',
                'covers': 'All iPad models'
            }
        ]
    },
    'printer': {
        'name': 'Printer',
        'icon': '🖨️',
        'environmental_impact': 'Printers contain a complex mix of plastics, metals, and circuit boards. Ink and toner cartridges are particularly problematic — a single cartridge takes up to 1,000 years to decompose. Australia disposes of over 3 million cartridges per week, the vast majority going to landfill.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Clear stored documents and fax logs',
                'detail': 'Many modern printers store document histories and scanned images. Access the printer\'s menu and clear all stored jobs and logs.'
            },
            {
                'step': 2,
                'title': 'Remove and separately recycle ink/toner cartridges',
                'detail': 'Take out all ink or toner cartridges. These must be recycled separately — most office supply stores accept them for free.'
            },
            {
                'step': 3,
                'title': 'Factory reset the printer',
                'detail': 'Use the printer\'s control panel to restore factory settings. This clears stored Wi-Fi passwords, user credentials, and any saved configurations.'
            },
            {
                'step': 4,
                'title': 'Remove stored network credentials',
                'detail': 'Confirm that Wi-Fi settings, passwords, and any linked cloud printing accounts have been cleared.'
            },
            {
                'step': 5,
                'title': 'Remove paper trays and accessories',
                'detail': 'Remove paper trays, dust covers, and any add-on accessories. These may be recyclable separately or useful to someone else.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'TechCollect',
                'description': 'Accepts printers and multifunction devices at 600+ locations Australia-wide for free.',
                'url': 'https://techcollect.com.au',
                'covers': 'Printers, scanners, multifunction devices'
            },
            {
                'name': 'Cartridges 4 Planet Ark',
                'description': 'Free recycling for ink and toner cartridges at 4,000+ drop-off points including Australia Post.',
                'url': 'https://www.planetark.org/programs/cartridges-4-planet-ark',
                'covers': 'All brands of ink and toner cartridges'
            },
            {
                'name': 'Officeworks Cartridge Recycling',
                'description': 'Drop off cartridges at any Officeworks store for free recycling.',
                'url': 'https://www.officeworks.com.au',
                'covers': 'Ink and toner cartridges of all brands'
            }
        ]
    },
    'monitor': {
        'name': 'Monitor / TV',
        'icon': '🖥️',
        'environmental_impact': 'CRT monitors contain up to 4kg of lead — one of the most hazardous e-waste items in existence. Modern LCD and LED screens contain mercury in fluorescent backlights. Both types require specialist recycling to prevent toxic contamination of soil and water.',
        'sanitisation_steps': [
            {
                'step': 1,
                'title': 'Check for smart TV data',
                'detail': 'If this is a smart TV or monitor with built-in apps, sign out of all streaming services (Netflix, Stan, Disney+) and smart home integrations.'
            },
            {
                'step': 2,
                'title': 'Factory reset smart TVs',
                'detail': 'Navigate to Settings → System → Reset → Factory Reset to clear all account data, saved apps, and preferences.'
            },
            {
                'step': 3,
                'title': 'For standard monitors: no data to wipe',
                'detail': 'A standard computer monitor without smart features stores no personal data. Simply disconnect and prepare for recycling.'
            },
            {
                'step': 4,
                'title': 'Remove cables and stands if separating',
                'detail': 'HDMI, DisplayPort, and power cables can often be reused or recycled separately. Detachable stands may have separate recycling streams.'
            }
        ],
        'recycling_programs': [
            {
                'name': 'TechCollect',
                'description': 'Accepts monitors and TVs at 600+ locations across Australia for free.',
                'url': 'https://techcollect.com.au',
                'covers': 'CRT monitors, LCD/LED monitors, televisions'
            },
            {
                'name': 'Council Bulk Waste Collection',
                'description': 'Many councils accept TVs and monitors during scheduled bulk waste collections. Check your council website.',
                'url': 'https://www.sustainability.vic.gov.au',
                'covers': 'Large electronics including TVs'
            }
        ]
    }
}


@app.route('/')
def index():
    return render_template('index.html', devices=DEVICES)


@app.route('/result', methods=['POST'])
def result():
    device_key = request.form.get('device')
    if device_key not in DEVICES:
        return render_template('index.html', devices=DEVICES, error="Please select a valid device.")
    device = DEVICES[device_key]
    return render_template('result.html', device=device, device_key=device_key)


if __name__ == '__main__':
    app.run(debug=True)
