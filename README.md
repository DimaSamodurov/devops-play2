## Playing with AWS roles

### Task
Create script to
- take an instance as input 
- change (show/add/remove) security groups for the instance
- get the IAM role of the instance and attach another policy to that role.

### Run 

List Security groups:

    python play2.py --list_sg --i "i-05546040079c6c2ad"
    
    