# import sys, os, boto3

# def verify_task():
#     username = os.getenv('KODEARENA_USERNAME', 'LOCAL_USER')
#     repo_name = f"webapp-repo-{username}"
#     print("-" * 40); print("AWS RESOURCE VERIFICATION REPORT"); print("-" * 40)
#     aws_region = 'eu-west-2'
#     for r in ['eu-west-1', 'eu-west-2', 'eu-west-3']:
#         try:
#             temp_ecr = boto3.client('ecr', region_name=r)
#             temp_ecr.describe_repositories(repositoryNames=[repo_name])
#             aws_region = r
#             break
#         except Exception:
#             pass

#     try: ecr = boto3.client('ecr', region_name=aws_region)
#     except Exception as e: print(f"FAILED: Could not connect to AWS. Error: {e}"); return
    
#     try:
#         repos = ecr.describe_repositories(repositoryNames=[repo_name])
#         repo = repos['repositories'][0]
#         print("TC1 [ECR Exists] (2/2) - Success: Verified.")
        
#         if repo.get('imageTagMutability') == 'IMMUTABLE': print("TC2 [Mutability] (1/1) - Success: Verified.")
#         else: print("TC2 [Mutability] (0/1) - Failed.")
            
#         if repo.get('imageScanningConfiguration', {}).get('scanOnPush') == True: print("TC5 [Vulnerability Scan] (1/1) - Success: Verified.")
#         else: print("TC5 [Vulnerability Scan] (0/1) - Failed.")
            
#         imgs = ecr.describe_images(repositoryName=repo_name)['imageDetails']
#         if len(imgs) > 0:
#             print("TC3 [Image Exists] (2/2) - Success: Verified.")
#             img = imgs[0]
#             if len(img.get('imageTags', [])) > 0: print("TC4 [Image Tagged] (2/2) - Success: Verified.")
#             else: print("TC4 [Image Tagged] (0/2) - Failed.")
                
#             if img.get('imageManifestMediaType') or img.get('artifactMediaType'): print("TC6 [Architecture Valid] (2/2) - Success: Verified.")
#             else: print("TC6 [Architecture Valid] (0/2) - Failed.")
#         else:
#             print("TC3 [Image Exists] (0/2) - Failed.")
#             print("TC4 [Image Tagged] (0/2) - Failed.")
#             print("TC6 [Architecture Valid] (0/2) - Failed.")
            
#     except:
#         print("TC1 [ECR Exists] (0/2) - Failed.")
#         print("TC2 [Mutability] (0/1) - Failed.")
#         print("TC3 [Image Exists] (0/2) - Failed.")
#         print("TC4 [Image Tagged] (0/2) - Failed.")
#         print("TC5 [Vulnerability Scan] (0/1) - Failed.")
#         print("TC6 [Architecture Valid] (0/2) - Failed.")

#     print("-" * 40)

# if __name__ == "__main__":
#     verify_task()



import sys, os, boto3

def get_possible_usernames():
    prefixes = []
    # 1. From sys.argv
    if len(sys.argv) > 1 and sys.argv[1].strip():
        prefixes.append(sys.argv[1].strip())
    
    # 2. From platform environment variables
    env_vars = [
        'KODEBUCK_USERNAME',
        'KODEARENA_USERNAME',
        'LABSKRAFT_USERNAME',
        'CANDIDATE_PREFIX',
        'CANDIDATE_EMAIL',
        'KODEBUCK_USER',
        'KODEARENA_USER',
        'LABSKRAFT_USER',
        'USER',
        'USERNAME'
    ]
    for env in env_vars:
        val = os.getenv(env)
        if val and val.strip():
            val = val.strip()
            prefixes.append(val)
            if '@' in val:
                prefixes.append(val.split('@')[0])

    # 3. From AWS STS IAM username
    try:
        sts = boto3.client('sts')
        arn = sts.get_caller_identity().get('Arn', '')
        iam_user = None
        if ':user/' in arn:
            iam_user = arn.split(':user/')[-1].strip()
        elif ':assumed-role/' in arn:
            role_part = arn.split(':assumed-role/')[-1].strip()
            iam_user = role_part.split('/')[-1].strip() if '/' in role_part else role_part.strip()
        if iam_user and iam_user not in ['root', 'ubuntu', 'administrator', 'SYSTEM', 'LOCAL_USER']:
            prefixes.append(iam_user)
            if 'labs-kraft-' in iam_user:
                prefixes.append(iam_user.replace('labs-kraft-', ''))
            elif '-' in iam_user:
                prefixes.append(iam_user.split('-')[-1])
    except Exception:
        pass

    candidates = []
    for p in prefixes:
        p_clean = p.strip()
        if p_clean and p_clean not in ['root', 'ubuntu', 'administrator', 'SYSTEM']:
            for variant in [p_clean, p_clean.lower()]:
                if variant not in candidates:
                    candidates.append(variant)
    if 'LOCAL_USER' not in candidates:
        candidates.append('LOCAL_USER')
    return candidates

def find_ecr_repository():
    regions = []
    default_reg = os.getenv('AWS_DEFAULT_REGION') or os.getenv('AWS_REGION')
    if default_reg:
        regions.append(default_reg)
    for r in ['eu-west-1', 'eu-west-2', 'eu-west-3', 'us-east-1', 'us-east-2']:
        if r not in regions:
            regions.append(r)

    candidate_prefixes = get_possible_usernames()
    possible_repo_names = [f"webapp-repo-{p}" for p in candidate_prefixes]
    possible_repo_names.append("webapp-repo")

    # Pass 1: Describe all repositories in each region to auto-discover
    for r in regions:
        try:
            client = boto3.client('ecr', region_name=r)
            resp = client.describe_repositories()
            all_repos = resp.get('repositories', [])
            
            # Exact match with candidate name
            for repo in all_repos:
                name = repo.get('repositoryName', '')
                if name in possible_repo_names or name.lower() in [x.lower() for x in possible_repo_names]:
                    return client, r, repo
            
            # Any repository starting with webapp-repo
            for repo in all_repos:
                name = repo.get('repositoryName', '')
                if name.startswith('webapp-repo'):
                    return client, r, repo

            # Any repository containing webapp
            for repo in all_repos:
                name = repo.get('repositoryName', '')
                if 'webapp' in name.lower():
                    return client, r, repo

            # If only 1 repository in the candidate's account
            if len(all_repos) == 1:
                return client, r, all_repos[0]
        except Exception:
            pass

    # Pass 2: Query specific repository names if describe_repositories without args was restricted
    for r in regions:
        try:
            client = boto3.client('ecr', region_name=r)
            for name in possible_repo_names:
                try:
                    resp = client.describe_repositories(repositoryNames=[name])
                    if resp.get('repositories'):
                        return client, r, resp['repositories'][0]
                except Exception:
                    continue
        except Exception:
            pass

    fallback_region = default_reg or 'eu-west-1'
    return boto3.client('ecr', region_name=fallback_region), fallback_region, None

def verify_task():
    print("-" * 40)
    print("AWS RESOURCE VERIFICATION REPORT")
    print("-" * 40)

    try:
        ecr, aws_region, repo = find_ecr_repository()
    except Exception as e:
        print(f"FAILED: Could not connect to AWS. Error: {e}")
        return

    repo_name = repo.get('repositoryName') if repo else None

    # TC1: ECR Repository Existence
    if repo:
        print("TC1 [ECR Exists] (2/2) - Success: Verified.")
    else:
        print("TC1 [ECR Exists] (0/2) - Failed.")

    # TC2: ECR Repository configured with Mutability constraints (IMMUTABLE)
    if repo and repo.get('imageTagMutability') == 'IMMUTABLE':
        print("TC2 [Mutability] (1/1) - Success: Verified.")
    else:
        print("TC2 [Mutability] (0/1) - Failed.")

    # Image details for TC3, TC4, TC6
    imgs = []
    if repo and repo_name:
        try:
            imgs = ecr.describe_images(repositoryName=repo_name).get('imageDetails', [])
        except Exception:
            imgs = []

    # TC3: ECR Repository contains at least one Image
    # TC4: Image is correctly tagged
    if len(imgs) > 0:
        print("TC3 [Image Exists] (2/2) - Success: Verified.")
        img = imgs[0]
        if len(img.get('imageTags', [])) > 0:
            print("TC4 [Image Tagged] (2/2) - Success: Verified.")
        else:
            print("TC4 [Image Tagged] (0/2) - Failed.")
    else:
        print("TC3 [Image Exists] (0/2) - Failed.")
        print("TC4 [Image Tagged] (0/2) - Failed.")

    # TC5: Vulnerability Scan
    if repo and repo.get('imageScanningConfiguration', {}).get('scanOnPush') is True:
        print("TC5 [Vulnerability Scan] (1/1) - Success: Verified.")
    else:
        print("TC5 [Vulnerability Scan] (0/1) - Failed.")

    # TC6: Docker Image architecture is standard
    if len(imgs) > 0:
        img = imgs[0]
        if img.get('imageManifestMediaType') or img.get('artifactMediaType'):
            print("TC6 [Architecture Valid] (2/2) - Success: Verified.")
        else:
            print("TC6 [Architecture Valid] (0/2) - Failed.")
    else:
        print("TC6 [Architecture Valid] (0/2) - Failed.")

    print("-" * 40)

if __name__ == "__main__":
    verify_task()

