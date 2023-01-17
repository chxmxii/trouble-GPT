from ansible.module_utils.basic import AnsibleModule
import json
import requests

def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(required=True, type='str'),
            path=dict(required=False, type='str', default=None)
        ),
        supports_check_mode=True
    )

    api_key = module.params['api_key']
    path = module.params['path']

    # API request to the troubleshoot endpoint
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    prompt = module.params['error_message']
    data = {
        'prompt': prompt,
        'model': 'text-davinci-002',
        'stop': '.',
        'max_tokens':1024
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.post(url, json=data, headers=headers)

    # check the response status code
    if response.status_code != 200:
        module.fail_json(msg="Failed to get troubleshoot information from chatGPT, please check the API key.")

    troubleshoot_info = response.json()['choices'][0]['text']
    if path:
        with open(path, 'w') as f:
            f.write(troubleshoot_info)
    else:
       module.exit_json(ansible_facts={'troubleshoot_info': troubleshoot_info}, changed=True)

if __name__ == '__main__':
    main()
