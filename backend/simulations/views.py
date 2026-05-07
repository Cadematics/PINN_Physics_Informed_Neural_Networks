from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
from django.conf import settings

# Add the project root to sys.path so we can import from solvers
project_root = settings.BASE_DIR.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from solvers.diffusion_1d_numerical import DiffusionSolver

@csrf_exempt
def numerical_diffusion_view(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            alpha = data.get('alpha', 110)
            nx = data.get('nx', 100)
            nt = data.get('nt', 400)
            time_steps = data.get('time_steps', nt)
            length = data.get('length', 100)
            total_time = data.get('total_time', 4)
            
        elif request.method == "GET":
            alpha = float(request.GET.get('alpha', 110))
            nx = int(request.GET.get('nx', 100))
            nt = int(request.GET.get('nt', 400))
            time_steps = int(request.GET.get('time_steps', nt))
            length = float(request.GET.get('length', 100))
            total_time = float(request.GET.get('total_time', 4))
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        solver = DiffusionSolver(
            alpha=alpha, 
            nx=nx, 
            time_steps=time_steps,
            length=length,
            total_time=total_time
        )
        results = solver.solve()
        return JsonResponse(results, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
