from base64 import decode
from distutils.log import debug
import winrm
import re
import logging


# FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
# logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class HyperV:
    def __init__(
        self,
        env_prefix = "",
        storage_root = '''C:\\template.vmcx''',
        vm_template_pach = '',
        host = '',
        user = '',
        password = '',
        debug = False
    ) -> None:

        self.env_prefix = env_prefix
        self.storage_root = storage_root
        self.vm_template_pach = vm_template_pach

        self.host = host
        self.user = user
        self.password = password

        self.debug = debug

        # Создаём сессию для работы с гипервизором
        self.session = winrm.Session(self.host, auth=(self.user, self.password))


    # Запрос свободной памяти на гипервизоре
    @property
    def get_free_memory(self):
        
        ps = "(Get-WMIObject Win32_OperatingSystem).FreePhysicalMemory / 1MB"
        r = self.session.run_ps(ps)
        if r.status_code == 0:
            free_memory = round(float(r.std_out.decode('utf-8').replace(',','.')), 2)
        else:
            return False
        return free_memory

    # Поиск шаблона vmcx в папке с шаблоном виртуальной машины
    @property
    def get_vmcx(self):
        ps_script = f"Get-ChildItem -Path '{self.vm_template_pach}' -Include *.vmcx -File -Recurse -ErrorAction SilentlyContinue"
        logging.debug(f'ps_script: {ps_script}')
        vmcx = self.session.run_ps(ps_script)
        result = re.findall(r'[\w-]*.vmcx', vmcx.std_out.decode('utf-8'))[0]
        logging.debug(f'result: {result}')
        return result

    # Поиск имени шаблона виртуалки
    def get_template_name(self, vmcx):
        ps_script = f"""
        $TempVM = (Compare-VM -Path '{self.vm_template_pach}\Virtual Machines\{vmcx}').VM
        $TempVM | Select VMName | Select -ExpandProperty "VMName"
        """
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(r.std_out.decode('utf-8').split("\r\n"))
        result = r.std_out.decode('utf-8').split("\r\n")[0]
        logging.debug(f'result: {result}')
        return result
    
    # Проверка наличия папки у виртуальной машины
    def path_exists(self, vm_name=''):
        vm_patch=f"{self.storage_root}\{self.env_prefix}\{vm_name}"
        ps_script =  f'Test-Path -Path "{vm_patch}"'
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if 'True' in r.std_out.decode('utf-8'):
            return True
        return False
    
    # Удаление папки виртуальной машины
    def path_remove(self, vm_name=''):
        vm_patch=f"{self.storage_root}\{self.env_prefix}\{vm_name}"
        ps_script =  f'Remove-Item "{vm_patch}" -Recurse'
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == '1':
            return False
        return True
    
    def vm_exists(self, vm_name=''):
        ps_script =  f'Get-VM -Name "{ vm_name }"| Select -ExpandProperty Name'
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        vm_find_name = r.std_out.decode('utf-8').strip()
        if vm_name == vm_find_name:
            return True
        return False
    
    # Импорт виртуалок
    def import_vm(self, vm_name='', template_name='', vmcx =''):
        if vmcx == '':
            vmcx = self.get_vmcx
        if template_name == '':
            template_name = self.get_template_name(vmcx)
        
        import_from=f"{self.vm_template_pach}\Virtual Machines\{vmcx}"
        vm_patch=f"{self.storage_root}\{self.env_prefix}\{vm_name}"
        vm_name=f"{vm_name}"

        # Генерируем powershell скрипт
        ps_script =  (
        f"Import-VM -Path '{import_from}' `\n"
            f"-Copy -GenerateNewId `\n"
            f"-SnapshotFilePath '{vm_patch}' `\n"
            f"-VhdDestinationPath '{vm_patch}' `\n"
            f"-SmartPagingFilePath '{vm_patch}'"
        )
        
        logging.debug(f'ps_script: \n{ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == 0:
            return True
        logging.error(f"std_err:\n{r.std_err.decode('utf-8')}")
        return False

    # Переименование виртуальной машины
    def vm_rename(self, old_name='', new_name=''):
        ps_script = f"Rename-VM '{old_name}' -NewName '{new_name}'"
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == '1':
            return False
        return True

    # Изменение виртуальной машины
    def vm_set(self, vm='', cpu='', ram=''):
        ps_script = f'Set-VM -Name "{vm}" -ProcessorCount {cpu} -StaticMemory -MemoryStartupBytes {ram}Gb'
        logging.debug(f'ps_script: {ps_script}')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == 0:
            return True
        logging.error(f"std_err:\n{r.std_err.decode('utf-8')}")
        return False


    # Включение виртуалок
    def vm_start(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Start-VM')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == 0:
            return True
        logging.error(f"std_err:\n{r.std_err.decode('utf-8')}")
        return False

    # Выключение виртуалок
    def vm_stop(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Stop-VM', force=True)
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == 0:
            return True
        logging.error(f"std_err:\n{r.std_err.decode('utf-8')}")
        return False

    # Поставить машины на паузу по маске или передав список машин
    def vm_suspend(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Suspend-VM')
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == 0:
            return True
        logging.error(f"std_err:\n{r.std_err.decode('utf-8')}")
        return False

    # Поставить машины на паузу по маске или передав список машин
    def vm_restart(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Restart-VM', force=True)
        r = self.session.run_ps(ps_script)
        logging.debug(f'status_code: {r.status_code}')
        logging.debug(f"std_out: {r.std_out.decode('utf-8')}")
        if r.status_code == '1':
            return False
        return True
    
    
    # Снять машины с паузы по маске или передав список машин
    def vm_resume(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Resume-VM')
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out: {result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code \n{result.status_code}")
        if result.status_code == '1':
            return False
        return True

    # Статус машин
    def vm_state(self, vms=[]):
        state_keys = ['state', 'cpu', 'memory', 'uptime' ]
        ps_script = self.gen_job(vms_list=vms, job='Get-VM')
        logging.debug(f'ps_script \n{ps_script}')
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out\n{result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code \n{result.status_code}")
        if result.status_code == '1':
            return False
                
        r_result = {}
        r = re.findall(r"[\s-]+\r\n([\w\W]*$)", result.std_out.decode('utf-8'))
        for line in r[0].splitlines():
            if line:
                r_result.setdefault(line.split()[0], dict(zip(state_keys, (line.split()[1:5]))))
        return r_result
    
    # Генерирует PS более/менее стандартные скрипты
    def gen_job(self, job, vms_list=[], **kwargs):
        params = ''
        if kwargs:
            if 'create_snapshot' in kwargs.keys(): params = f"-SnapshotName {kwargs['create_snapshot']}"
            if 'get_snapshot' in kwargs.keys(): params = f"| Get-VMSnapshot"
            if 'current_snapshot' in kwargs.keys(): params = f"| select Name, ParentSnapshotName"
            if 'dellete_snapshots' in kwargs.keys(): params = f"| Remove-VMSnapshot -Name {kwargs['dellete_snapshots']}"
            if 'apply_snapshots' in kwargs.keys(): params = f"| Restore-VMSnapshot -Name  {kwargs['apply_snapshots']} -Confirm:$false"
            
            if 'force' in kwargs.keys():
                params = '-Force'

        all_vms = f"{self.env_prefix}* "

        if vms_list:
            logging.debug('vms_list not is empty')
            all_vms = ", ".join(str(f'"{x}"') for x in vms_list)

        ps_script = f"{job} -Name {all_vms} {params}"
        logging.debug(f'ps_script: {ps_script}')
        return ps_script
    
    # Создать снапшот машин по маске или передав список машин
    def snapshot_create(self, snapshot_name='Clear_OS', vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Checkpoint-VM', create_snapshot = snapshot_name)
        logging.debug(f'ps_script \n{ps_script}')
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out\n{result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code \n{result.status_code}")
        if result.status_code == '1':
            return False
        return True
    
    # Список снапшотов виртуалных машин 
    def snapshot_get_all(self, vms=[]):
        state_keys = ['name', 'type', 'creation_date', 'creation_time', 'parent_snapshot' ]
        ps_script = self.gen_job(vms_list=vms, job='Get-VM', get_snapshot = True)
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out: {result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code \n{result.status_code}")
        if result.status_code == '1':
            return False
        
        r_result = {}
        r = re.findall(r"[\s-]+\r\n([\w\W]*$)", result.std_out.decode('utf-8'))
        for line in r[0].splitlines():
            if line:
                # r_result.setdefault(line.split()[0], []).append(line.split()[1:])
                r_result.setdefault(line.split()[0], []).append(dict(zip(state_keys, (line.split()[1:]))))
        return r_result

    # Получить текущие снапшоты виртуальных машин
    def snapshot_get_current(self, vms=[]):
        ps_script = self.gen_job(vms_list=vms, job='Get-VM', current_snapshot = True)
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out: {result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code \n{result.status_code}")
        if result.status_code == '1':
            return False
        r_result = {}
        for line in result.std_out.decode('utf-8').splitlines():
            if line and not 'Name' in line and not '----' in line:
                r_result.setdefault(line.split()[0],line.split()[1:][0])
        return r_result
    
    # Удалить снапшоты
    def snapshot_rm(self, vms=[], snapshot_name=''):
        ps_script = self.gen_job(vms_list=vms, job='Get-VM', dellete_snapshots = snapshot_name)
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out: {result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code: {result.status_code}")
        if result.status_code == '1':
            return False
        return True

    def snapshot_apply(self, vms=[], snapshot_name=''):
        ps_script = self.gen_job(vms_list=vms, job='Get-VM', apply_snapshots = snapshot_name)
        result = self.session.run_ps(ps_script)
        logging.debug(f"result std_out: {result.std_out.decode('utf-8')}")
        logging.debug(f"result status_code: {result.status_code}")
        if result.status_code == '1':
            return False
        return True


